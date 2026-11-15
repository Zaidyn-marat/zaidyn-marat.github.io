import os
import glob
import re
import yaml
import requests

MEMBERS_DIR = "src/content/members"
PUBS_DIR = "src/content/publications"
MAILTO = "your-lab@example.edu"

# 1. 把 Timur（及其他非本组方向合作者）的 ORCID 填在这里，抓取时直接跳过
EXCLUDED_ORCIDS = {
    "0000-0002-2389-2262",
    "0009-0005-7254-524X",
}

# 2. 剔除与本组无关的跨组合作方向关键词（全小写匹配）
# OFF_TOPIC_KEYWORDS = [
#     "cubesat", "antenna", "x-band", "l/s band", "антенна", "микрожолақты",
#     "fpga", "modulo", "cryptograph", "divider", "polynomial multiplier",
#     "speech", "speaker", "voice activity", "ultrashort utterances", "голоса",
#     "energy harvester", "igzo", "zno/por-si", "nanofilms", "air-showers"
# ]

def get_member_orcids():
    orcids = set()
    for filepath in glob.glob(f"{MEMBERS_DIR}/*.md"):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if match:
                meta = yaml.safe_load(match.group(1))
                if meta and meta.get("orcid"):
                    oid = meta["orcid"].strip()
                    if oid not in EXCLUDED_ORCIDS:
                        orcids.add(oid)
    return list(orcids)


def fetch_and_save():
    orcids = get_member_orcids()
    if not orcids:
        print("No valid ORCIDs found.")
        return

    os.makedirs(PUBS_DIR, exist_ok=True)
    orcid_filter = "|".join(orcids)
    url = f"https://api.openalex.org/works?filter=author.orcid:{orcid_filter}&per-page=150&mailto={MAILTO}"
    
    res = requests.get(url).json()
    works = res.get("results", [])

    saved_count = 0
    for work in works:
        # if not is_relevant(work):
        #     continue

        doi_url = work.get("doi")
        if not doi_url:
            continue

        doi_clean = doi_url.replace("https://doi.org/", "").lower()
        safe_filename = re.sub(r'[^a-z0-9\-_.]', '_', doi_clean) + ".md"
        filepath = os.path.join(PUBS_DIR, safe_filename)

        title = (work.get("title") or "Untitled").replace('"', '\\"')
        year = work.get("publication_year") or 2026
        
        loc = work.get("primary_location") or {}
        source = loc.get("source") or {}
        journal = (source.get("display_name") or "Preprint / arXiv").replace('"', '\\"')

        authorships = work.get("authorships", [])
        authors_list = [a["author"]["display_name"] for a in authorships if a.get("author")]
        authors_str = ", ".join(authors_list[:5]) + ", et al." if len(authors_list) > 6 else ", ".join(authors_list)

        md_content = f"""---
title: "{title}"
authors: "{authors_str}"
journal: "{journal}"
year: {year}
doi: "{doi_url}"
---
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        saved_count += 1

    print(f"Done! Saved {saved_count} clean publications.")

if __name__ == "__main__":
    fetch_and_save()