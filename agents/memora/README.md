# Memora 🧠

> Zero-config LLM memory that understands context, not just text.

Memora is a smart memory layer for your AI applications. Unlike traditional vector databases that store text as isolated chunks, Memora captures **concepts**, **relationships**, and **domains** — so your LLM gets the full picture with 90% fewer tokens.

---

## ✨ Why Memora?

| Feature | Pinecone | ChromaDB | **Memora** |
|---------|----------|----------|------------|
| Setup | Cloud signup + API key | `pip install` | `pip install memora-memory` ✅ |
| Dedup | ❌ Manual | ❌ Manual | ✅ **Auto-merge (semantic)** |
| Hybrid Search | ❌ Vector only | ❌ Vector only | ✅ **BM25 + Vector** |
| Domain Filter | ❌ Manual metadata | ❌ Manual metadata | ✅ **Auto-detect (v8)** |
| Related Memories | ❌ No | ❌ No | ✅ **Auto-bonding** |
| Auto-aging | ❌ No | ❌ No | ✅ **Fractal compression** |
| Session Memory | ❌ No | ❌ No | ✅ **Auto-expire** |
| **Dynamic Domains** | ❌ No | ❌ No | ✅ **AUTO-DOMAIN v2** |
| Token Cost | ~2000/query | ~2000/query | **~50/query** ✅ |

---

## 🚀 Quick Start

### Install
```bash
pip install git+https://github.com/SPARKEDIX/memora.git


pip install memora-memory
```

### Basic Usage
```python
import memora

# Create memory
memory = memora.Memory()

# Store memories - domains created AUTOMATICALLY
memory.add("Mujhe diabetes hai, fasting 180", user="rahul")
memory.add("Main roz 6 baje walk karta hoon", user="rahul")
memory.add("Doctor ne Metformin 500mg diya hai", user="rahul")

# Retrieve context - domain auto-detected from query
context = memory.get("Walk ke baad kya khaana chahiye?", user="rahul")
print(context)
```

**Output:**
```
Primary:
    Main roz 6 baje walk karta hoon

Related:
    Mujhe diabetes hai, fasting 180
    Doctor ne Metformin 500mg diya hai
```

**Your LLM now gets the full health context — not just the "walk" keyword.**

---

## 🌟 What's New in v8: AUTO-DOMAIN v2 + Scalability Fixes

Memora v8 introduces **completely dynamic domain creation** — no hardcoded keywords, no manual config. Also fixes critical bugs from v7: semantic dedup, domain explosion, domain filtering in queries.

```python
memory = memora.Memory()

# These 3 texts → automatically create "health" domain
memory.add("Diabetes blood sugar 180 mg/dL", user="rahul")
memory.add("Metformin 500mg twice daily", user="rahul")
memory.add("Insulin dosage adjusted", user="rahul")

# These 3 texts → automatically create "coding" domain
memory.add("Python code for ML model", user="rahul")
memory.add("Code review for PR #42", user="rahul")
memory.add("Debug production bug in API", user="rahul")

# These 3 texts → automatically create "gaming" domain
memory.add("PUBG ranked match chicken dinner", user="rahul")
memory.add("Elden Ring boss fight guide", user="rahul")
memory.add("Steam summer sale games", user="rahul")

# Query auto-detects domain
memory.get("diabetes treatment")    # → searches health domain
memory.get("programming bug")       # → searches coding domain
memory.get("gaming headset")        # → searches gaming domain

# Rename domains later for readability
memory.rename_domain("domain_1", "health")
memory.rename_domain("domain_2", "coding")
memory.rename_domain("domain_3", "gaming")

# List all domains
memory.list_domains()
# [{'name': 'health', 'count': 3}, {'name': 'coding', 'count': 3}, {'name': 'gaming', 'count': 3}]
```

### How AUTO-DOMAIN v2 Works

```
Text → Embedding → Compare with ALL domain centroids (cosine similarity)
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            similarity ≥ 0.50      similarity < 0.50
                    │                   │
                    ▼                   ▼
         Assign to existing         Add to "unassigned"
         domain, update            pool. When 3 similar
         centroid (weighted        texts accumulate
         average)                  → create NEW domain
                                       (centroid = avg of 3)
                    │
                    ▼
        Every 20 inserts:
        • Merge weak domains (<3 memories)
        • Merge similar domains (>0.60 centroid sim)
        • Re-check unassigned pool
```

---

## 📖 Full API Reference

### `Memory(db_path="memory.db", default_ttl="30d")`

Create a memory instance.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `db_path` | `str` | `"memory.db"` | SQLite file path for storage |
| `default_ttl` | `str` | `"30d"` | Default expiration (`"7d"`, `"30d"`, `"forever"`) |

**Example:**
```python
# Separate DB per user
rahul_mem = memora.Memory(db_path="rahul.db")
priya_mem = memora.Memory(db_path="priya.db")
```

---

### `memory.add(text, user=None, ttl=None, session=False)`

Store a memory. **Domain auto-detected/created.**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | **Required** | The text to store |
| `user` | `str` | `None` | Owner of this memory (isolated per user) |
| `ttl` | `str` | `None` | Time-to-live (`"7d"`, `"30d"`, `"forever"`, `None` = use default) |
| `session` | `bool` | `False` | If `True`, auto-delete after 1 hour |

**Examples:**
```python
# Permanent health record
memory.add("Mujhe diabetes hai", user="rahul", ttl="forever")

# Temporary chat
memory.add("Aaj mausam accha hai", user="rahul", ttl="7d")

# Session-only (disappears after session)
memory.add("OTP is 123456", user="rahul", session=True)

# Batch insert
memory.add_many(["text1", "text2", "text3"], user="rahul")
```

---

### `memory.get(query, user=None, domain=None, top_k=5, include_bonded=True)`

Retrieve relevant memories. **Domain auto-detected from query if not specified.**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | **Required** | Your search query |
| `user` | `str` | `None` | Filter by specific user |
| `domain` | `str` | `None` | Force specific domain (skip auto-detect) |
| `top_k` | `int` | `5` | Number of primary results |
| `include_bonded` | `bool` | `True` | Include related memories from same domain |

**Examples:**
```python
# Basic query - domain auto-detected
result = memory.get("Walk ke baad kya khaana?", user="rahul")

# Force specific domain
result = memory.get("Diet plan", user="rahul", domain="health")

# More results
result = memory.get("Health tips", user="rahul", top_k=10)

# Latent vector mode (for downstream ML)
vectors = memory.get("health query", mode="latent")
```

**Returns (text mode):**
```
Primary:
    [Most relevant memories]

Related:
    [Bonded memories from same domain]
```

---

### `memory.list_domains()`

List all domains with memory counts.

```python
domains = memory.list_domains()
# [{'name': 'health', 'count': 15}, {'name': 'coding', 'count': 10}, ...]
```

---

### `memory.rename_domain(old_name, new_name)`

Give meaningful names to auto-generated domains.

```python
memory.rename_domain("domain_1", "health")
memory.rename_domain("domain_2", "work_projects")
memory.rename_domain("domain_3", "gaming_rpg")
# Returns True if successful
```

---

### `memory.delete(user=None, domain=None, older_than=None)`

Delete memories.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user` | `str` | `None` | Delete all memories of this user |
| `domain` | `str` | `None` | Delete only this domain |
| `older_than` | `str` | `None` | Delete memories older than (`"30d"`, `"90d"`, `"1y"`) |

**Examples:**
```python
# Delete all casual chats
memory.delete(user="rahul", domain="casual")

# Delete everything older than 1 year
memory.delete(user="rahul", older_than="1y")

# Wipe everything
memory.delete()
```

---

### `memory.optimize()`

Merge similar memories to reduce storage.

```python
# After adding many similar memories
memory.optimize()
# Reduces crystal count by 30-50%
```

---

### `memory.info()`

Get database stats including unassigned pool.

```python
print(memory.info())
# {
#     'total_memories': 50,
#     'unique_users': 3,
#     'domains': {'health': 20, 'coding': 15, 'gaming': 10},
#     'levels': {0: 30, 1: 15, 2: 5},
#     'unassigned': 3,
#     'index_size': 45,
#     'persisted': True
# }
```

---

### `memory.export(path)` / `memory.import_data(path, merge=False)`

Backup and restore memories.

```python
# Export
memory.export("backup.json")

# Import (replace existing)
memory.import_data("backup.json")

# Import (merge with existing)
memory.import_data("backup.json", merge=True)
```

---

## 🏥 Real-World Example: Health Assistant

```python
import memora
from openai import OpenAI

llm = OpenAI()
memory = memora.Memory(db_path="patients.db")

def doctor_chat(patient_id, message):
    # 1. Retrieve patient history (domain auto-detected)
    context = memory.get(message, user=patient_id, top_k=3)

    # 2. Ask LLM with context
    response = llm.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Dr.AI. Use patient history."},
            {"role": "user", "content": f"History:\n{context}\n\nPatient: {message}"}
        ]
    )

    reply = response.choices[0].message.content

    # 3. Store both sides permanently
    memory.add(message, user=patient_id, ttl="forever")
    memory.add(reply, user=patient_id, ttl="forever")

    return reply

# Usage
print(doctor_chat("rahul_123", "Mujhe diabetes hai, fasting 180"))
print(doctor_chat("rahul_123", "Main roz walk karta hoon"))
print(doctor_chat("rahul_123", "Walk ke baad kya khaana chahiye?"))
# Output: Diabetes-aware diet advice
```

---

## 🧠 How It Works (v8)

```
Your Text
    ↓
Sentence-Transformers (all-MiniLM-L6-v2 → 384-dim)
    ↓
AUTO-DOMAIN v2 Engine:
    ├─ Compare embedding with ALL domain centroids
    ├─ similarity ≥ 0.50 → assign, update centroid (weighted avg)
    ├─ similarity < 0.50 → unassigned pool
    ├─ 3 similar in pool → create NEW domain (centroid = avg of 3)
    └─ Every 20 inserts: merge weak/similar domains, re-check pool
    ↓
Store in:
    ├─ FAISS IVF Index (fast vector search, O(√n))
    ├─ BM25 Index (exact keyword matching)
    └─ SQLite (metadata + domains table + unassigned table)
    ↓
When you query:
    Hybrid Search (FAISS + BM25 merged)
    ↓
    Domain Filter (auto-detected or forced)
    ↓
    Crystal Bonding (surface related from same domain)
    ↓
    Fractal Aging (level 0→1→2→3: compress over time)
    ↓
    Formatted Context → Your LLM
```

---

## 📊 v7 vs v8 Comparison

| Metric | v7 | **v8 (Fixed)** |
|--------|-----|----------------|
| 30 memories added | 46 crystals (dedup broken) | **27 crystals** |
| Exact duplicate | New ID | **Same ID returned** |
| Semantic duplicate | Not merged | **Merged (sim ≥ 0.60)** |
| Domain count (30 mixed) | 8 (explosion) | **4 (reasonable)** |
| Health query result | Mixed work/gaming | **Health only** |
| Storage (30 mem) | 163 KB | **158 KB** |
| Query speed | O(n) | **O(√n) via IVF** |

---

## 📦 Installation

```bash
pip install git+https://github.com/SPARKEDIX/memora.git
```

**Dependencies:** `sentence-transformers`, `faiss-cpu`, `numpy`, `rank-bm25`

---

## 🧪 Run Validation Tests

```bash
python tests/validation_test.py
```

---

## 📝 License

MIT License — free for personal and commercial use.

---

## 🙏 Support

- ⭐ Star this repo if you find it useful
- 🐛 Open an issue for bugs
- 💡 Open a discussion for feature requests

---

**Made with ❤️ for smarter AI memories.**
