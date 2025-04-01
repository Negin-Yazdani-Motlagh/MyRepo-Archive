import os
import json
import pandas as pd
import re
from collections import defaultdict
from tqdm import tqdm

# === FILE PATHS ===
base_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Yearly"
dict_v91 = os.path.join(base_path, "Dictionary of soft skills (9.1).xlsx")
json_input = os.path.join(base_path, "Yearly_Job_Posts_2016_2020.json")
output_path = os.path.join(base_path, "v91_AllOccurrences_2016_2020.json")

# === LOAD DICTIONARY ===
dict_df = pd.read_excel(dict_v91)
dict_df.columns = dict_df.columns.str.strip().str.lower()

sub_to_head = {
    str(row["subcategory"]).strip().lower(): str(row["headcategory"]).strip().lower()
    for _, row in dict_df.iterrows()
    if pd.notna(row["subcategory"]) and pd.notna(row["headcategory"])
}

# === COMPILE REGEX PATTERNS ===
pattern_map = {
    sub: (re.compile(rf"\b{re.escape(sub)}\b", re.IGNORECASE), head)
    for sub, head in sub_to_head.items()
}

# === LOAD POSTS ===
with open(json_input, "r", encoding="utf-8") as f:
    yc_data = json.load(f).get("YC", {})

# === PROCESS OCCURRENCES ===
results = {}
for year in tqdm(sorted(yc_data.keys()), desc="Counting V9.1 Skills (2016–2020)"):
    comments = yc_data[year].get("comments", [])
    year_counts = defaultdict(int)

    for comment in comments:
        text = comment.lower()
        for sub, (pattern, head) in pattern_map.items():
            year_counts[head] += len(pattern.findall(text))

    results[year] = {
        "total_job_posts": len(comments),
        "soft_skill_counts": dict(year_counts)
    }

# === SAVE OUTPUT ===
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print(f"✅ Saved v9.1 (2016–2020) results to: {output_path}")
