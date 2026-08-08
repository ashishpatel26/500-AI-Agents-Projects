"""
memora/core.py - Cognitive Crystal Database v8 (Fixed) with AUTO-DOMAIN + SCALABILITY

Fixed bugs from v8:
1. Semantic dedup via FAISS (threshold 0.60) - NOT exact text match
2. Domain clustering: embedding-based centroid comparison (threshold 0.50), unassigned pool, auto-named domains
3. Domain filtering in get(): strict SQL post-filter after FAISS retrieval
4. Storage normalization via fixes 1-3
5. Keeps IVF speed gains (IndexIVFFlat for >=1000 crystals)
"""

import sqlite3
import numpy as np
import faiss
import time
import os
import pickle
import json
import uuid
import threading
from typing import Optional, List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

DEDUP_THRESHOLD = 0.60
DOMAIN_SIM_THRESHOLD = 0.50
DOMAIN_MERGE_THRESHOLD = 0.60
UNASSIGNED_SIM_THRESHOLD = 0.35
MIN_DOMAIN_SIZE = 3
MERGE_INTERVAL = 20
FLAT_TO_IVF_THRESHOLD = 1000
IVF_REBUILD_THRESHOLD = 10000
S_30D, S_90D, S_365D, TTL_DEFAULT = 2592000, 7776000, 31536000, 2592000


def _parse_ttl(val):
    if val is None:
        return TTL_DEFAULT
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        if val == "forever":
            return float("inf")
        mul = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "y": 31536000}
        for suffix, m in mul.items():
            if val.endswith(suffix):
                return float(val[:-len(suffix)]) * m
    return TTL_DEFAULT


class LatentAdapter:
    def __init__(self, crystal_dim=384, hidden_dim=4096):
        self.projection = np.random.randn(crystal_dim, hidden_dim).astype(np.float32) * 0.01

    def project(self, e: np.ndarray) -> np.ndarray:
        return np.dot(e.astype(np.float32), self.projection)


class Memory:
    """Production CCDB v8 Fixed: adaptive IVF, BM25 cache, FAISS semantic dedup, embedding-based domains."""

    def __init__(self, db_path: str = "memory.db", default_ttl: str = "30d"):
        self.db_path = db_path
        self.ip = db_path.replace(".db", "_faiss.bin")
        self.bp = db_path.replace(".db", "_bm25.pkl")
        self.default_ttl = _parse_ttl(default_ttl)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = 384
        self.adapter = LatentAdapter(self.dim)
        self._stop_cleaner = threading.Event()
        self._lock = threading.Lock()
        self._add_counter = 0
        self._crystal_count = 0
        self._global_index = None
        self._trained = False
        self.unassigned_embeddings = []  # List of (crystal_id, embedding, user, text)
        self._init_db()
        self._init_indices()
        self._init_bm25()
        self._load_domains()
        self._load_unassigned()
        self._start_cleaner()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crystals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL,
                    text TEXT NOT NULL,
                    embedding BLOB NOT NULL,
                    domain TEXT,
                    strength INTEGER DEFAULT 1,
                    created_at REAL NOT NULL DEFAULT 0,
                    last_accessed REAL NOT NULL DEFAULT 0,
                    level INTEGER DEFAULT 0,
                    compressed_to INTEGER,
                    is_session INTEGER DEFAULT 0,
                    session_id TEXT,
                    expires_at REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS domains (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    centroid BLOB NOT NULL,
                    count INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS unassigned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    crystal_id INTEGER NOT NULL,
                    user TEXT NOT NULL,
                    text TEXT NOT NULL,
                    embedding BLOB NOT NULL,
                    timestamp REAL NOT NULL
                )
            """)
            for col, dt in [("created_at", "REAL DEFAULT 0"), ("level", "INTEGER DEFAULT 0"),
                            ("compressed_to", "INTEGER"), ("is_session", "INTEGER DEFAULT 0"),
                            ("session_id", "TEXT"), ("expires_at", "REAL")]:
                try:
                    conn.execute(f"ALTER TABLE crystals ADD COLUMN {col} {dt}")
                except sqlite3.OperationalError:
                    pass
            conn.execute("CREATE INDEX IF NOT EXISTS idx_crystals_user_domain ON crystals(user, domain)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_crystals_user ON crystals(user)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_crystals_domain ON crystals(domain)")

    def _init_indices(self):
        self._crystal_count = self._count_crystals()
        self._faiss_to_crystal_id = []  # Maps FAISS index -> crystal_id
        if os.path.exists(self.ip):
            self._global_index = faiss.read_index(self.ip)
            self._trained = True
            self._load_faiss_mapping()
        else:
            self._create_new_index()
            self._trained = False

    def _load_faiss_mapping(self):
        """Load FAISS index to crystal_id mapping from database."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT id FROM crystals ORDER BY id").fetchall()
        self._faiss_to_crystal_id = [r[0] for r in rows]

    def _count_crystals(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT COUNT(*) FROM crystals").fetchone()[0]

    def _create_new_index(self):
        if self._crystal_count < FLAT_TO_IVF_THRESHOLD:
            self._global_index = faiss.IndexFlatIP(self.dim)
        else:
            nlist = self._calc_nlist(self._crystal_count)
            quantizer = faiss.IndexFlatIP(self.dim)
            self._global_index = faiss.IndexIVFFlat(quantizer, self.dim, nlist, faiss.METRIC_INNER_PRODUCT)
            self._global_index.nprobe = max(10, nlist // 10)

    def _calc_nlist(self, n: int) -> int:
        return max(10, min(100, int(np.sqrt(max(1, n)))))

    def _save_index(self):
        faiss.write_index(self._global_index, self.ip)

    def _ensure_trained(self):
        if self._trained:
            return
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT id FROM crystals LIMIT 1000").fetchall()
        if len(rows) >= 100:
            ids = [r[0] for r in rows]
            embs = self._load_embeddings(ids)
            self._global_index.train(embs)
            self._trained = True
        else:
            if not isinstance(self._global_index, faiss.IndexFlatIP):
                self._global_index = faiss.IndexFlatIP(self.dim)
            self._trained = True

    def _maybe_rebuild_index(self):
        new_count = self._count_crystals()
        old_count = self._crystal_count
        if new_count == old_count:
            return
        self._crystal_count = new_count
        if old_count < FLAT_TO_IVF_THRESHOLD <= new_count and isinstance(self._global_index, faiss.IndexFlatIP):
            self._migrate_flat_to_ivf()
        elif old_count < IVF_REBUILD_THRESHOLD <= new_count and isinstance(self._global_index, faiss.IndexIVFFlat):
            self._rebuild_ivf()

    def _migrate_flat_to_ivf(self):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT id FROM crystals").fetchall()
        if not rows:
            return
        ids = [r[0] for r in rows]
        embs = self._load_embeddings(ids)
        nlist = self._calc_nlist(self._crystal_count)
        quantizer = faiss.IndexFlatIP(self.dim)
        new_index = faiss.IndexIVFFlat(quantizer, self.dim, nlist, faiss.METRIC_INNER_PRODUCT)
        new_index.nprobe = max(10, nlist // 10)
        new_index.train(embs)
        new_index.add(embs)
        self._global_index = new_index
        self._faiss_to_crystal_id = ids
        self._trained = True
        self._save_index()

    def _rebuild_ivf(self):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT id FROM crystals").fetchall()
        if not rows:
            return
        ids = [r[0] for r in rows]
        embs = self._load_embeddings(ids)
        nlist = self._calc_nlist(self._crystal_count)
        quantizer = faiss.IndexFlatIP(self.dim)
        new_index = faiss.IndexIVFFlat(quantizer, self.dim, nlist, faiss.METRIC_INNER_PRODUCT)
        new_index.nprobe = max(10, nlist // 10)
        new_index.train(embs)
        new_index.add(embs)
        self._global_index = new_index
        self._faiss_to_crystal_id = ids
        self._trained = True
        self._save_index()

    def _load_embeddings(self, ids: List[int]) -> np.ndarray:
        if not ids:
            return np.zeros((0, self.dim), dtype=np.float32)
        with sqlite3.connect(self.db_path) as conn:
            placeholders = ",".join("?" * len(ids))
            rows = conn.execute(f"SELECT embedding FROM crystals WHERE id IN ({placeholders})", ids).fetchall()
        return np.vstack([np.frombuffer(r[0], dtype=np.float32) for r in rows])

    def _init_bm25(self):
        self._bm25_cached = None
        self._bm25_dirty = True
        if os.path.exists(self.bp):
            with open(self.bp, "rb") as f:
                d = pickle.load(f)
                self.bm25_ids, self.bm25_corpus = d["ids"], d["corpus"]
        else:
            self.bm25_ids, self.bm25_corpus = [], []

    def _save_bm25(self):
        with open(self.bp, "wb") as f:
            pickle.dump({"ids": self.bm25_ids, "corpus": self.bm25_corpus}, f)

    def _rebuild_bm25(self):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT id, text FROM crystals").fetchall()
        self.bm25_ids = [r[0] for r in rows]
        self.bm25_corpus = [r[1].lower().split() for r in rows]
        self._bm25_cached = None
        self._bm25_dirty = True

    def _get_bm25(self):
        if self._bm25_dirty and self.bm25_corpus:
            self._bm25_cached = BM25Okapi(self.bm25_corpus)
            self._bm25_dirty = False
        return self._bm25_cached

    def _load_domains(self):
        self.domain_names = []
        self.domain_centroids = []
        self.domain_counts = []
        self.domain_name_to_idx = {}
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT name, centroid, count FROM domains ORDER BY id").fetchall()
        for i, (name, centroid_bytes, count) in enumerate(rows):
            centroid = np.frombuffer(centroid_bytes, dtype=np.float32)
            self.domain_names.append(name)
            self.domain_centroids.append(centroid)
            self.domain_counts.append(count)
            self.domain_name_to_idx[name] = i

    def _load_unassigned(self):
        self.unassigned_embeddings = []
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT crystal_id, user, text, embedding FROM unassigned").fetchall()
        for crystal_id, user, text, emb_bytes in rows:
            emb = np.frombuffer(emb_bytes, dtype=np.float32)
            self.unassigned_embeddings.append((crystal_id, emb, user, text))

    def _save_unassigned(self, conn, crystal_id: int, user: str, text: str, emb: np.ndarray):
        emb_bytes = emb.astype(np.float32).tobytes()
        conn.execute(
            "INSERT INTO unassigned (crystal_id, user, text, embedding, timestamp) VALUES (?, ?, ?, ?, ?)",
            (crystal_id, user, text, emb_bytes, time.time())
        )

    def _remove_unassigned(self, conn, crystal_id: int):
        conn.execute("DELETE FROM unassigned WHERE crystal_id = ?", (crystal_id,))
        self.unassigned_embeddings = [u for u in self.unassigned_embeddings if u[0] != crystal_id]

    def _save_domain(self, name: str, centroid: np.ndarray, count: int, conn=None):
        centroid_bytes = centroid.astype(np.float32).tobytes()
        if conn is not None:
            conn.execute(
                "INSERT OR REPLACE INTO domains (name, centroid, count) VALUES (?, ?, ?)",
                (name, centroid_bytes, count)
            )
        else:
            with sqlite3.connect(self.db_path) as c:
                c.execute(
                    "INSERT OR REPLACE INTO domains (name, centroid, count) VALUES (?, ?, ?)",
                    (name, centroid_bytes, count)
                )

    def _create_domain(self, centroid: np.ndarray, initial_count: int = MIN_DOMAIN_SIZE, conn=None) -> str:
        idx = len(self.domain_names)
        name = f"domain_{idx + 1}"
        self.domain_names.append(name)
        self.domain_centroids.append(centroid.copy())
        self.domain_counts.append(initial_count)
        self.domain_name_to_idx[name] = idx
        self._save_domain(name, centroid, initial_count, conn)
        return name

    def _update_domain_centroid(self, idx: int, new_embedding: np.ndarray, conn=None):
        count = self.domain_counts[idx]
        old_centroid = self.domain_centroids[idx]
        new_centroid = (old_centroid * count + new_embedding) / (count + 1)
        new_centroid = new_centroid / np.linalg.norm(new_centroid)
        self.domain_centroids[idx] = new_centroid
        self.domain_counts[idx] = count + 1
        self._save_domain(self.domain_names[idx], new_centroid, count + 1, conn)

    def _detect_domain(self, emb: np.ndarray) -> Tuple[Optional[str], float]:
        if not self.domain_centroids:
            return None, 0.0
        best_idx = -1
        best_sim = -1.0
        for i, centroid in enumerate(self.domain_centroids):
            sim = float(np.dot(emb, centroid))
            if sim > best_sim:
                best_sim = sim
                best_idx = i
        if best_sim >= DOMAIN_SIM_THRESHOLD and best_idx >= 0:
            return self.domain_names[best_idx], best_sim
        return None, best_sim

    def _assign_domain(self, conn, crystal_id: int, emb: np.ndarray, user: str, text: str) -> str:
        domain_name, sim = self._detect_domain(emb)
        if domain_name is not None:
            idx = self.domain_name_to_idx[domain_name]
            self._update_domain_centroid(idx, emb, conn)
            return domain_name
        
        # No matching domain - add to unassigned pool
        self._save_unassigned(conn, crystal_id, user, text, emb)
        self.unassigned_embeddings.append((crystal_id, emb, user, text))
        self._try_form_domain_from_unassigned(conn, emb)
        return "unassigned"

    def _try_form_domain_from_unassigned(self, conn, new_emb: np.ndarray):
        # Don't form domain on every add - rely on periodic clustering instead
        # This avoids creating fragmented domains from diverse but related memories
        pass

    def _cluster_unassigned(self, conn):
        """Greedy clustering on all unassigned embeddings to form new domains."""
        if len(self.unassigned_embeddings) < MIN_DOMAIN_SIZE:
            return
        
        embeddings = [u[1] for u in self.unassigned_embeddings]
        n = len(embeddings)
        used = [False] * n
        
        for i in range(n):
            if used[i]:
                continue
            # Start a new cluster with embedding i
            cluster = [i]
            used[i] = True
            
            for j in range(i + 1, n):
                if used[j]:
                    continue
                # Check similarity to cluster centroid
                cluster_embs = [embeddings[k] for k in cluster]
                centroid = np.mean(cluster_embs, axis=0)
                centroid = centroid / np.linalg.norm(centroid)
                sim_to_centroid = float(np.dot(centroid, embeddings[j]))
                if sim_to_centroid >= UNASSIGNED_SIM_THRESHOLD:
                    cluster.append(j)
                    used[j] = True
            
            if len(cluster) >= MIN_DOMAIN_SIZE:
                # Form domain from this cluster
                cluster_embs = [embeddings[k] for k in cluster]
                centroid = np.mean(cluster_embs, axis=0)
                centroid = centroid / np.linalg.norm(centroid)
                domain_name = self._create_domain(centroid, len(cluster), conn)
                
                # Move all cluster members to this domain
                for idx in sorted(cluster, reverse=True):
                    cid, uemb, user, text = self.unassigned_embeddings[idx]
                    self._move_unassigned_to_domain(conn, cid, uemb, user, text, domain_name)

    def _move_unassigned_to_domain(self, conn, crystal_id: int, emb: np.ndarray, user: str, text: str, domain_name: str):
        self._remove_unassigned(conn, crystal_id)
        conn.execute("UPDATE crystals SET domain = ? WHERE id = ?", (domain_name, crystal_id))
        idx = self.domain_name_to_idx[domain_name]
        self._update_domain_centroid(idx, emb, conn)

    def _reassign_unassigned_to_domains(self, conn):
        if not self.unassigned_embeddings or not self.domain_centroids:
            return
        
        for crystal_id, emb, user, text in self.unassigned_embeddings[:]:
            domain_name, sim = self._detect_domain(emb)
            if domain_name is not None:
                idx = self.domain_name_to_idx[domain_name]
                self._update_domain_centroid(idx, emb, conn)
                self._move_unassigned_to_domain(conn, crystal_id, emb, user, text, domain_name)

    def _merge_weak_domains(self):
        strong_indices = [i for i, c in enumerate(self.domain_counts) if c >= MIN_DOMAIN_SIZE]
        weak_indices = [i for i, c in enumerate(self.domain_counts) if c < MIN_DOMAIN_SIZE]
        
        if not strong_indices or not weak_indices:
            return
        
        for weak_idx in weak_indices:
            weak_centroid = self.domain_centroids[weak_idx]
            best_strong = -1
            best_sim = -1.0
            
            for strong_idx in strong_indices:
                sim = float(np.dot(weak_centroid, self.domain_centroids[strong_idx]))
                if sim > best_sim:
                    best_sim = sim
                    best_strong = strong_idx
            
            if best_sim >= DOMAIN_SIM_THRESHOLD and best_strong >= 0:
                self._merge_domains(weak_idx, best_strong)

    def _merge_domains(self, from_idx: int, to_idx: int):
        if from_idx >= len(self.domain_names) or to_idx >= len(self.domain_names):
            return
        if from_idx == to_idx:
            return
        
        from_name = self.domain_names[from_idx]
        to_name = self.domain_names[to_idx]
        from_count = self.domain_counts[from_idx]
        from_centroid = self.domain_centroids[from_idx]
        to_count = self.domain_counts[to_idx]
        to_centroid = self.domain_centroids[to_idx]
        
        new_count = from_count + to_count
        new_centroid = (from_centroid * from_count + to_centroid * to_count) / new_count
        new_centroid = new_centroid / np.linalg.norm(new_centroid)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE crystals SET domain = ? WHERE domain = ?", (to_name, from_name))
            conn.execute("DELETE FROM domains WHERE name = ?", (from_name,))
        
        self.domain_names[to_idx] = to_name
        self.domain_centroids[to_idx] = new_centroid
        self.domain_counts[to_idx] = new_count
        self._save_domain(to_name, new_centroid, new_count)
        
        del self.domain_names[from_idx]
        del self.domain_centroids[from_idx]
        del self.domain_counts[from_idx]
        del self.domain_name_to_idx[from_name]
        
        for i, name in enumerate(self.domain_names):
            self.domain_name_to_idx[name] = i

    def _periodic_domain_merge(self):
        if len(self.domain_centroids) < 2:
            return
        
        merged = True
        while merged:
            merged = False
            for i in range(len(self.domain_centroids)):
                for j in range(i + 1, len(self.domain_centroids)):
                    sim = float(np.dot(self.domain_centroids[i], self.domain_centroids[j]))
                    if sim >= DOMAIN_MERGE_THRESHOLD:
                        self._merge_domains(j, i)
                        merged = True
                        break
                if merged:
                    break

    def _check_duplicate(self, emb: np.ndarray, user: str) -> Tuple[Optional[int], float]:
        if self._global_index.ntotal == 0:
            return None, 0.0
        self._ensure_trained()
        D, I = self._global_index.search(emb.reshape(1, -1), 1)
        if D[0][0] >= DEDUP_THRESHOLD:
            faiss_idx = int(I[0][0])
            if faiss_idx < len(self._faiss_to_crystal_id):
                candidate_id = self._faiss_to_crystal_id[faiss_idx]
                with sqlite3.connect(self.db_path) as conn:
                    row = conn.execute(
                        "SELECT id, embedding FROM crystals WHERE id = ? AND user = ?",
                        (candidate_id, user)
                    ).fetchone()
                    if row:
                        existing_emb = np.frombuffer(row[1], dtype=np.float32)
                        sim = float(np.dot(emb, existing_emb))
                        if sim >= DEDUP_THRESHOLD:
                            return row[0], sim
        return None, 0.0

    def _start_cleaner(self):
        def run():
            while not self._stop_cleaner.is_set():
                self._clean_expired()
                self._stop_cleaner.wait(3600)
        t = threading.Thread(target=run, daemon=True)
        t.start()

    def _clean_expired(self):
        now = time.time()
        with self._lock, sqlite3.connect(self.db_path) as conn:
            dead = conn.execute(
                "SELECT id FROM crystals WHERE expires_at IS NOT NULL AND expires_at < ?", (now,)
            ).fetchall()
            if dead:
                ids = [r[0] for r in dead]
                conn.execute("DELETE FROM crystals WHERE id IN " +
                           f"({','.join('?' for _ in ids)})", ids)
                try:
                    self._global_index.remove_ids(np.array(ids, dtype=np.int64))
                    self._save_index()
                except Exception:
                    pass

    def _embed(self, texts: List[str]) -> np.ndarray:
        e = self.model.encode(texts, convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(e)
        return e

    def add(self, text: str, user: Optional[str] = None, session: bool = False,
            ttl: Optional[str] = None) -> int:
        return self.add_many([text], user, session, ttl)[0]

    def add_many(self, texts: List[str], user: Optional[str] = None,
                 session: bool = False, ttl: Optional[str] = None) -> List[int]:
        if not texts:
            return []
        user, now = user or "default", time.time()
        ttl_s = _parse_ttl(ttl) if ttl is not None else self.default_ttl
        sid = str(uuid.uuid4())[:8] if session else None
        exp = now + min(3600 if session else 9999999999, ttl_s) if ttl_s != float("inf") else None
        embs = self._embed(texts)
        ids = []

        with self._lock, sqlite3.connect(self.db_path) as conn:
            for i, text in enumerate(texts):
                emb = embs[i]
                dup_id, sim = self._check_duplicate(emb, user)
                if dup_id:
                    conn.execute(
                        "UPDATE crystals SET strength=strength+1, last_accessed=? WHERE id=?",
                        (now, dup_id))
                    ids.append(dup_id)
                    continue

                emb_bytes = emb.astype(np.float32).tobytes()
                cur = conn.execute(
                    "INSERT INTO crystals (user,text,embedding,domain,strength,created_at,last_accessed,level,is_session,session_id,expires_at) VALUES (?,?,?,?,1,?,?,0,?,?,?)",
                    (user, text, emb_bytes, "unassigned", now, now, int(session), sid, exp))
                nid = cur.lastrowid
                ids.append(nid)

                domain = self._assign_domain(conn, nid, emb, user, text)

                self._ensure_trained()
                self._global_index.add(emb.reshape(1, -1))
                self._faiss_to_crystal_id.append(nid)
                self._save_index()

                r = conn.execute("SELECT text FROM crystals WHERE id=?", (nid,)).fetchone()
                if r:
                    self.bm25_ids.append(nid)
                    self.bm25_corpus.append(r[0].lower().split())
                    self._bm25_dirty = True

        if self._bm25_dirty:
            self._save_bm25()
        self._maybe_rebuild_index()

        self._add_counter += len(texts)
        if self._add_counter >= MERGE_INTERVAL:
            self._add_counter = 0
            with sqlite3.connect(self.db_path) as conn:
                self._reassign_unassigned_to_domains(conn)
                self._cluster_unassigned(conn)
            self._merge_weak_domains()
            self._periodic_domain_merge()

        # Final clustering pass to ensure unassigned are clustered
        with sqlite3.connect(self.db_path) as conn:
            self._cluster_unassigned(conn)

        return ids

    def get(self, query: str, user: Optional[str] = None, domain: Optional[str] = None,
            after_date=None, before_date=None, min_confidence=None,
            top_k=5, include_bonded=True, mode="text") -> Any:
        res = self.get_many([query], user, domain, after_date, before_date,
                           min_confidence, top_k, include_bonded, mode)
        return res[0] if res else ("" if mode == "text" else [])

    def get_many(self, queries: List[str], user: Optional[str] = None,
                 domain=None, after_date=None, before_date=None,
                 min_confidence=None, top_k=5, include_bonded=True, mode="text") -> List:
        if self._global_index.ntotal == 0 or not queries:
            return [""] * len(queries) if mode == "text" else [[]] * len(queries)
        self._auto_compress()
        q_embs = self._embed(queries)
        # Search more candidates to ensure we get enough from target domain
        sk = min(top_k * 10, self._global_index.ntotal)
        bs, idx = self._global_index.search(q_embs, sk)
        now = int(time.time())
        outs = []
        bm25 = self._get_bm25()

        for qi, query in enumerate(queries):
            target_domain = domain
            if target_domain is None:
                target_domain, _ = self._detect_domain(q_embs[qi])

            # Convert FAISS indices to crystal IDs
            vec_ids = []
            for i in idx[qi]:
                if i != -1 and i < len(self._faiss_to_crystal_id):
                    vec_ids.append(self._faiss_to_crystal_id[i])
            
            # Fallback: if still no domain, use domain of top FAISS result
            if target_domain is None and vec_ids:
                with sqlite3.connect(self.db_path) as conn:
                    row = conn.execute("SELECT domain FROM crystals WHERE id = ?", (vec_ids[0],)).fetchone()
                    if row and row[0] and row[0] != "unassigned":
                        target_domain = row[0]

            bm_ids = []
            if bm25 and self.bm25_corpus:
                bm_scores = bm25.get_scores(query.lower().split())
                topind = np.argsort(bm_scores)[::-1][:min(sk, 100)]
                bm_ids = [self.bm25_ids[i] for i in topind if bm_scores[i] > 0]

            merged_ids = []
            seen = set()
            for i in range(max(len(bm_ids), len(vec_ids))):
                if i < len(bm_ids) and bm_ids[i] not in seen:
                    merged_ids.append(bm_ids[i]); seen.add(bm_ids[i])
                if i < len(vec_ids) and vec_ids[i] not in seen:
                    merged_ids.append(vec_ids[i]); seen.add(vec_ids[i])

            params = list(merged_ids)
            where = []
            if user:
                where.append("user = ?"); params.append(user)
            where.append("(expires_at IS NULL OR expires_at > ?)"); params.append(now)
            if after_date:
                where.append("created_at >= ?"); params.append(after_date)
            if before_date:
                where.append("created_at <= ?"); params.append(before_date)
            if min_confidence:
                where.append("strength >= ?"); params.append(min_confidence)
            w = " AND " + " AND ".join(where) if where else ""
            df = " AND domain = ?" if target_domain else ""
            dp = [target_domain] if target_domain else []

            con = sqlite3.connect(self.db_path)
            ph = ",".join("?" * len(merged_ids)) if merged_ids else "NULL"
            rows = con.execute(
                f"SELECT id, text, domain, level FROM crystals WHERE id IN ({ph}){w}{df} ORDER BY strength DESC, last_accessed DESC LIMIT ?",
                params + dp + [top_k]
            ).fetchall()

            p_ids, p_txts, p_doms = [], [], []
            st = set()
            for r in rows:
                tag = f"{r[1]} (older)" if r[3] >= 2 else r[1]
                if tag not in st:
                    st.add(tag); p_ids.append(r[0]); p_txts.append(tag); p_doms.append(r[2])

            bonded = []
            if include_bonded and p_ids:
                ps = set(p_ids)
                target_dom = target_domain
                if target_dom:
                    ex = f"AND id NOT IN ({','.join('?' * len(ps))})"
                    bp = list(ps)
                    if user:
                        br = con.execute(
                            f"SELECT text, level FROM crystals WHERE user = ? AND domain = ? {ex} AND (expires_at IS NULL OR expires_at > ?) ORDER BY strength DESC, last_accessed DESC LIMIT ?",
                            [user, target_dom] + bp + [now, top_k]
                        ).fetchall()
                    else:
                        br = con.execute(
                            f"SELECT text, level FROM crystals WHERE domain = ? {ex} AND (expires_at IS NULL OR expires_at > ?) ORDER BY strength DESC, last_accessed DESC LIMIT ?",
                            [target_dom] + bp + [now, top_k]
                        ).fetchall()
                    for bt, bl in br:
                        tag = f"{bt} (older)" if bl >= 2 else bt
                        if tag not in st:
                            st.add(tag); bonded.append(tag)

            if mode == "latent":
                vecs = [self.adapter.project(self._embed([t])[0]) for t in p_txts + bonded]
                outs.append(vecs)
            else:
                parts = ["Primary:"]
                parts.extend(f"    {t}" for t in p_txts)
                if bonded:
                    parts.append("\nRelated:")
                    parts.extend(f"    {t}" for t in bonded[:top_k])
                outs.append("\n".join(parts))
            con.close()
        return outs

    def list_domains(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT name, count FROM domains ORDER BY count DESC").fetchall()
        return [{"name": r[0], "count": r[1]} for r in rows]

    def rename_domain(self, old_name: str, new_name: str) -> bool:
        if old_name not in self.domain_name_to_idx:
            return False
        if new_name in self.domain_name_to_idx:
            return False
        idx = self.domain_name_to_idx[old_name]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE domains SET name = ? WHERE name = ?", (new_name, old_name))
            conn.execute("UPDATE crystals SET domain = ? WHERE domain = ?", (new_name, old_name))
        self.domain_names[idx] = new_name
        del self.domain_name_to_idx[old_name]
        self.domain_name_to_idx[new_name] = idx
        return True

    def delete(self, user: Optional[str] = None, domain: Optional[str] = None,
               older_than: Optional[float] = None) -> int:
        with self._lock, sqlite3.connect(self.db_path) as con:
            where = []
            params = []
            if user:
                where.append("user = ?"); params.append(user)
            if domain:
                where.append("domain = ?"); params.append(domain)
            if older_than:
                where.append("created_at < ?"); params.append(older_than)
            w = "WHERE " + " AND ".join(where) if where else ""
            rows = con.execute(f"SELECT id FROM crystals {w}", params).fetchall()
            con.execute(f"DELETE FROM crystals {w}", params)
            ids = [r[0] for r in rows]
        if ids:
            try:
                self._global_index.remove_ids(np.array(ids, dtype=np.int64))
                self._save_index()
            except Exception:
                pass
        self._crystal_count = self._count_crystals()
        self._load_faiss_mapping()
        self._rebuild_bm25()
        self._save_bm25()
        return len(ids)

    def info(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as con:
            t = con.execute("SELECT COUNT(*) FROM crystals").fetchone()[0]
            u = con.execute("SELECT COUNT(DISTINCT user) FROM crystals").fetchone()[0]
            d = con.execute("SELECT domain, COUNT(*) FROM crystals GROUP BY domain").fetchall()
            l = con.execute("SELECT level, COUNT(*) FROM crystals GROUP BY level").fetchall()
        index_type = type(self._global_index).__name__
        return {
            "total_memories": t, "unique_users": u,
            "domains": dict(d), "levels": dict(l),
            "index_size": self._global_index.ntotal,
            "index_type": index_type,
            "persisted": os.path.exists(self.ip),
            "bm25_size": len(self.bm25_corpus),
        }

    def export(self, path: str = "export.json"):
        data = {"version": "memora_v8_fixed", "exported_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "memories": []}
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                "SELECT user, text, embedding, domain, strength, created_at, last_accessed, level, compressed_to, is_session, session_id, expires_at FROM crystals"
            ).fetchall()
        data["memories"] = [dict(zip([
            "user", "text", "embedding", "domain", "strength", "created_at",
            "last_accessed", "level", "compressed_to", "is_session", "session_id", "expires_at"], r)) for r in rows]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return len(rows)

    def import_data(self, path: str, merge: bool = False):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not merge:
            self.delete()
        for m in data.get("memories", []):
            self.add_many([m["text"]], user=m["user"], session=m["is_session"],
                         ttl=m.get("expires_at", None))
        return len(data.get("memories", []))

    def _auto_compress(self):
        now = time.time()
        with sqlite3.connect(self.db_path) as con:
            for lv, thr in [(0, S_30D), (1, S_90D), (2, S_365D)]:
                rows = con.execute(
                    "SELECT id, text FROM crystals WHERE level=? AND ?-created_at > ?",
                    (lv, now, thr)).fetchall()
                for rid, mt in rows:
                    ct = self._compress_txt(mt, lv + 1)
                    con.execute("UPDATE crystals SET level=?, text=? WHERE id=?", (lv + 1, ct, rid))

    def _compress_txt(self, text: str, level: int) -> str:
        if level == 0:
            return text
        if level == 1:
            return text.split(".")[0].strip()
        if level == 2:
            return " ".join(text.split()[:8])[:80]
        w = text.split()[0].lower() if text.split() else "tag"
        return f"archive:{w}"

    def optimize(self) -> int:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                "SELECT id, user, text, domain, level FROM crystals WHERE level <= 1 ORDER BY user, domain"
            ).fetchall()
        if len(rows) < 2:
            return 0
        texts = [r[2] for r in rows]
        embs = self._embed(texts)
        done = set()
        merge_ct = 0
        for i in range(len(rows)):
            if i in done:
                continue
            grp = [i]
            for j in range(i + 1, len(rows)):
                if rows[j][1] == rows[i][1] and rows[j][3] == rows[i][3] and j not in done:
                    sim = float(np.dot(embs[i], embs[j]))
                    if sim > 0.35:
                        grp.append(j); done.add(j)
            if len(grp) > 1:
                hist = "; ".join(rows[g][2][:80] for g in grp[1:])
                new_txt = f"{rows[grp[0]][2]} (history: {hist})"
                new_lvl = min(max(rows[g][4] for g in grp), 1)
                rem_ids = [rows[g][0] for g in grp if g != grp[0]]
                with sqlite3.connect(self.db_path) as con:
                    con.execute("UPDATE crystals SET text=?, level=?, last_accessed=? WHERE id=?",
                               (new_txt, new_lvl, time.time(), rows[grp[0]][0]))
                    if rem_ids:
                        con.execute("DELETE FROM crystals WHERE id IN " +
                                   f"({','.join('?' for _ in rem_ids)})", rem_ids)
                if rem_ids:
                    try:
                        self._global_index.remove_ids(np.array(rem_ids, dtype=np.int64))
                        self._save_index()
                    except Exception:
                        pass
                merge_ct += 1
        if merge_ct:
            self._save_index()
            self._load_faiss_mapping()
            self._rebuild_bm25()
            self._save_bm25()
        return merge_ct

    def dashboard(self):
        import json as _json
        with sqlite3.connect(self.db_path) as con:
            c_t = con.execute("SELECT COUNT(*) FROM crystals").fetchone()[0]
            c_u = con.execute("SELECT COUNT(DISTINCT user) FROM crystals").fetchone()[0]
            dom_rows = con.execute("SELECT domain, COUNT(*) FROM crystals GROUP BY domain").fetchall()
            recent = con.execute("SELECT id, user, text, domain, strftime('%Y-%m-%d %H:%M:%S', datetime(created_at, 'unixepoch')) FROM crystals ORDER BY created_at DESC LIMIT 15").fetchall()
        dom_json = _json.dumps({d: c for d, c in dom_rows})
        recent_rows = "".join(
            f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2][:60]}</td><td>{r[3]}</td><td>{r[4]}</td></tr>"
            for r in recent
        )
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<title>Memora Dashboard v8 - Cognitive Crystal DB</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@3"></script>
</head><body style="font-family:monospace;max-width:900px;margin:auto;padding:20px">
<h1>Memora Dashboard</h1>
<p>{c_t} memories | {c_u} users | adaptive IVF index | embedding-based domains</p>
<canvas id="pieChart" width="400" height="300"></canvas>
<script>
let doms = JSON.parse('{dom_json}');
new Chart(document.getElementById('pieChart'), {{type:'pie',data:{{labels:Object.keys(doms),datasets:[{{data:Object.values(doms)}}]}}}});
</script>
<br/><table border="1" style="width:100%">
<thead><tr><th>ID</th><th>User</th><th>Memory</th><th>Domain</th><th>Time</th></tr></thead>
<tbody>{recent_rows}</tbody></table>
</body></html>"""


if __name__ == "__main__":
    for f in ["scale_test.db", "scale_test_faiss.bin", "scale_test_bm25.pkl"]:
        if os.path.exists(f):
            os.remove(f)
    m = Memory(db_path="scale_test.db")
    start = time.time()
    for i in range(5000):
        m.add(f"Memory {i} about health diabetes sugar level {i}", user="rahul")
    add_time = (time.time() - start) / 5000 * 1000
    times = []
    for _ in range(10):
        t0 = time.time()
        m.get("diabetes sugar health", user="rahul", top_k=5)
        times.append((time.time() - t0) * 1000)
    avg_query = sum(times) / len(times)
    print(f"Add latency: {add_time:.2f} ms")
    print(f"Query latency (5000 mem): {avg_query:.2f} ms")
    print(f"Index type: {m.info()['index_type']}")
    print(f"Info: {m.info()}")