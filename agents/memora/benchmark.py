import memora
import time
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

print("=" * 60)
print("MEMORA vs VECTOR DBs - COMPARISON BENCHMARK")
print("=" * 60)

# ============================================
# SETUP: Test Data
# ============================================
test_memories = [
    "Mujhe diabetes hai, fasting 180 rehti hai",
    "Main roz subah 6 baje walk karta hoon, 30 minute",
    "Doctor ne mujhe Metformin 500mg diya hai",
    "Mujhe blood pressure bhi hai, 140/90",
    "Main gym jata hoon sham ko",
    "Mujhe thyroid ki problem hai",
    "Main yoga karta hoon roz subah",
    "Mera weight 85kg hai, height 5'10",
    "Main diabetic diet follow karta hoon",
    "Meri sugar level control mein hai ab",
    
    "Python code likhta hoon Django mein",
    "Mera project deadline agle hafte hai",
    "Main software engineer hoon 3 saal se",
    "Code review karta hoon roz team ka",
    "GitHub pe 50 repositories hain meri",
    "Main React sikh raha hoon abhi",
    "Database optimization ka kaam chal raha hai",
    "Microservices architecture design kar raha hoon",
    "CI/CD pipeline setup ki hai team ne",
    "Bug fix kiya hai production mein",
    
    "PUBG khelta hoon roz raat ko",
    "Call of Duty mein veteran level hoon",
    "Steam pe 100 games hain meri library mein",
    "Main esports tournament dekhna pasand karta hoon",
    "GTA V mein racing karta hoon",
    "Main online multiplayer khelta hoon",
    "Naya gaming laptop liya hai RTX 4060",
    "Discord pe gaming server manage karta hoon",
    "Main Twitch pe stream karta hoon",
    "Elden Ring khel raha hoon abhi",
]

queries = [
    ("diabetes walk medicine", "health"),
    ("python code project", "work"),
    ("PUBG game stream", "gaming"),
    ("health diet sugar", "health"),
]

n_memories = len(test_memories)
print(f"\nTest data: {n_memories} memories (10 health + 10 work + 10 gaming)")

# ============================================
# SYSTEM 1: NAIVE PYTHON LIST (Baseline)
# ============================================
print("\n" + "-" * 60)
print("SYSTEM 1: NAIVE PYTHON LIST SEARCH")
print("-" * 60)

naive_db = test_memories.copy()

def naive_search(query, top_k=5):
    words = query.lower().split()
    scores = []
    for mem in naive_db:
        score = sum(1 for w in words if w in mem.lower())
        scores.append((score, mem))
    scores.sort(reverse=True)
    return scores[:top_k]

start = time.time()
for q, expected in queries:
    naive_search(q)
naive_time = (time.time() - start) * 1000 / len(queries)

print(f"Query latency: {naive_time:.2f} ms")
print(f"Search type: O(n) string matching")
print(f"Storage: {sum(len(m) for m in naive_db)} bytes (raw text only)")
print("Limitation: No semantic understanding - 'diabetes' won't match 'sugar'")

# ============================================
# SYSTEM 2: FAISS-ONLY (Simulates Pinecone/Chroma Core)
# ============================================
print("\n" + "-" * 60)
print("SYSTEM 2: FAISS-ONLY (Pure Vector Search)")
print("Simulates: Pinecone, ChromaDB, Weaviate core")
print("-" * 60)

for f in ["faiss_only.db", "faiss_only_faiss.bin", "faiss_only_bm25.pkl"]:
    if os.path.exists(f):
        os.remove(f)

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(test_memories)

dim = embeddings.shape[1]
faiss_index = faiss.IndexFlatIP(dim)
faiss_index.add(embeddings)

def faiss_search(query, top_k=5):
    q_emb = model.encode([query])
    scores, indices = faiss_index.search(q_emb, top_k)
    return [(scores[0][i], test_memories[indices[0][i]]) for i in range(top_k)]

start = time.time()
for q, expected in queries:
    faiss_search(q)
faiss_time = (time.time() - start) * 1000 / len(queries)

faiss_storage = embeddings.nbytes / 1024
print(f"Query latency: {faiss_time:.2f} ms")
print(f"Search type: Cosine similarity on 384-dim vectors")
print(f"Storage: {faiss_storage:.2f} KB (vectors only, no metadata)")
print("Limitation: Isolated chunks - no domain awareness, no dedup")

# ============================================
# SYSTEM 3: MEMORA (Full System)
# ============================================
print("\n" + "-" * 60)
print("SYSTEM 3: MEMORA (FAISS + BM25 + Dedup + Domain)")
print("-" * 60)

for f in ["memora_compare.db", "memora_compare_faiss.bin", "memora_compare_bm25.pkl"]:
    if os.path.exists(f):
        os.remove(f)

m = memora.Memory(db_path="memora_compare.db")

start = time.time()
for i, mem in enumerate(test_memories):
    user = "rahul"
    m.add(mem, user=user)
add_time = (time.time() - start) * 1000 / n_memories

start = time.time()
memora_results = []
for q, expected in queries:
    r = m.get(q, user="rahul", top_k=5)
    memora_results.append(r)
memora_time = (time.time() - start) * 1000 / len(queries)

db_size = os.path.getsize("memora_compare.db") / 1024
faiss_size = os.path.getsize("memora_compare_faiss.bin") / 1024 if os.path.exists("memora_compare_faiss.bin") else 0
bm25_size = os.path.getsize("memora_compare_bm25.pkl") / 1024 if os.path.exists("memora_compare_bm25.pkl") else 0
total_storage = db_size + faiss_size + bm25_size

info = m.info()

print(f"Add latency: {add_time:.2f} ms per memory")
print(f"Query latency: {memora_time:.2f} ms")
print(f"Search type: Hybrid (FAISS vector + BM25 keyword + Domain filter)")
print(f"Storage: {total_storage:.2f} KB (DB + FAISS + BM25)")
print(f"Domains auto-detected: {len(info.get('domains', {}))}")
print(f"Total crystals: {info['total_memories']}")

# ============================================
# ACCURACY TEST: Domain Isolation
# ============================================
print("\n" + "-" * 60)
print("ACCURACY: DOMAIN ISOLATION TEST")
print("-" * 60)

print("\nQuery: 'diabetes walk medicine' (expects HEALTH memories)")

print("\nNaive List Top Result:")
r = naive_search("diabetes walk medicine", 1)
print(f"  -> {r[0][1][:50]}... (score: {r[0][0]})")

print("\nFAISS-Only Top Result:")
r = faiss_search("diabetes walk medicine", 1)
print(f"  -> {r[0][1][:50]}... (score: {r[0][0]:.3f})")

print("\nMemora Result:")
r = m.get("diabetes walk medicine", user="rahul", top_k=3)
print(f"  -> {str(r)[:200]}...")

# ============================================
# FINAL COMPARISON TABLE
# ============================================
print("\n" + "=" * 60)
print("FINAL COMPARISON")
print("=" * 60)

print(f"""
{'Metric':<25} {'Naive':<15} {'FAISS-Only':<15} {'Memora':<15}
{'-'*25} {'-'*15} {'-'*15} {'-'*15}
{'Query Speed':<25} {naive_time:.1f} ms{'':<6} {faiss_time:.1f} ms{'':<6} {memora_time:.1f} ms
{'Storage (30 mem)':<25} ~{sum(len(m) for m in test_memories)//1024} KB{'':<10} {faiss_storage:.1f} KB{'':<8} {total_storage:.1f} KB
{'Semantic Search':<25} {'No':<15} {'Yes':<15} {'Yes':<15}
{'Domain Awareness':<25} {'No':<15} {'No':<15} {'Yes':<15}
{'Auto-Dedup':<25} {'No':<15} {'No':<15} {'Yes':<15}
{'Hybrid Search':<25} {'No':<15} {'No':<15} {'Yes':<15}
{'Offline/Local':<25} {'Yes':<15} {'Yes':<15} {'Yes':<15}
{'Zero Config':<25} {'Yes':<15} {'Yes':<15} {'Yes':<15}
""")

print("=" * 60)
print("NOTES:")
print("- Naive = O(n) string match (what beginners build)")
print("- FAISS-Only = What Pinecone/Chroma do at core (vector only)")
print("- Memora = Your system (vector + keyword + domain + dedup)")
print("=" * 60)