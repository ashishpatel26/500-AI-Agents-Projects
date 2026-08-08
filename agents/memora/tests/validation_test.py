import memora, time, os

# Clean start
for f in ["fix_test.db", "fix_test_faiss.bin", "fix_test_bm25.pkl"]:
    if os.path.exists(f): os.remove(f)

m = memora.Memory(db_path="fix_test.db")

# Test data: 30 memories (10 health, 10 work, 10 gaming)
memories = [
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

# Add all
for mem in memories:
    m.add(mem, user="rahul")

info = m.info()
print("=== DEDUP TEST ===")
print(f"Total crystals: {info['total_memories']} (expected: <=30)")
if info['total_memories'] > 30:
    print("FAIL: Dedup broken")
else:
    print("PASS: Dedup working")

# Add exact duplicate
dup_id1 = m.add("Mujhe diabetes hai, fasting 180 rehti hai", user="rahul")
dup_id2 = m.add("Mujhe diabetes hai, fasting 180 rehti hai", user="rahul")
print(f"Duplicate IDs: {dup_id1}, {dup_id2} (should be SAME)")
if dup_id1 == dup_id2:
    print("PASS: Exact dup merged")
else:
    print("FAIL: Exact dup NOT merged")

# Add semantic duplicate
sem_id1 = m.add("Doctor ne Metformin diya hai", user="rahul")
sem_id2 = m.add("Mere doctor ne mujhe Metformin medicine di", user="rahul")
print(f"Semantic dup IDs: {sem_id1}, {sem_id2}")
if sem_id1 == sem_id2:
    print("PASS: Semantic dup merged")
else:
    print("INFO: Semantic dup NOT merged (acceptable if similarity < 0.60)")

print()
print("=== DOMAIN TEST ===")
print(f"Domain count: {len(info.get('domains', {}))} (expected: 3-6)")
print(f"Domains: {info.get('domains', {})}")
if len(info.get('domains', {})) <= 6:
    print("PASS: Domain count reasonable")
else:
    print("FAIL: Domain explosion")

print()
print("=== QUERY ACCURACY TEST ===")
q = "diabetes walk medicine"
result = m.get(q, user="rahul", top_k=5)
print(f"Query: '{q}'")
print(result)

# Check if result contains work/gaming memories in Primary
result_str = str(result).lower()
has_work = any(w in result_str for w in ["python", "code", "project", "software", "react", "database", "microservices", "ci/cd", "bug"])
has_gaming = any(w in result_str for w in ["pubg", "cod", "steam", "esports", "gta", "multiplayer", "laptop", "discord", "twitch", "elden"])

if has_work or has_gaming:
    print("FAIL: Domain mixing detected in health query!")
else:
    print("PASS: No domain mixing")

print()
print("=== STORAGE TEST ===")
db = os.path.getsize("fix_test.db")/1024
faiss = os.path.getsize("fix_test_faiss.bin")/1024 if os.path.exists("fix_test_faiss.bin") else 0
bm25 = os.path.getsize("fix_test_bm25.pkl")/1024 if os.path.exists("fix_test_bm25.pkl") else 0
print(f"Total: {db+faiss+bm25:.1f} KB (v7 was ~70KB for 30 mem)")

print()
print("=== SPEED TEST ===")
start = time.time()
for _ in range(10):
    m.get("diabetes sugar health", user="rahul")
qt = (time.time()-start)/10*1000
print(f"Query latency: {qt:.2f} ms")