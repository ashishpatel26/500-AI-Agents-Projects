---
*** Begin Patch
*** Update File: agents/17-recipe-agent/agent.py
@@
 def parse_json_response(text: str) -> dict:
     cleaned = text.strip()
     if cleaned.startswith("```"):
         cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
         cleaned = re.sub(r"\s*```$", "", cleaned)
-    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
+    # Use non-greedy match to avoid excessive CPU on very large outputs
+    match = re.search(r"\{.*?\}", cleaned, re.DOTALL)
     if match:
         cleaned = match.group(0)
     return json.loads(cleaned)
*** End Patch
