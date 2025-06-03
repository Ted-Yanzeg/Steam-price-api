#!/usr/bin/env python3
"""
scraper/fetch_games.py  (v2)
----------------------------
Fetch metadata and review summaries for the top N Steam games and save as CSV.

• Game pool: SteamSpy 'all' → 10k+ games → sort by owners and take top N
• Metadata: Steam Store API
• Review summary: /appreviews/{appid}?json=1&filter=summary
• Rate limiting: sleep interval is configurable; retry on failure (≤3 attempts)
• Supports --resume: if output CSV exists, skip already fetched appids
"""

import csv
import json
import os
import sys
import time
import argparse
import requests

from typing import Dict, Any, List, Optional
from datetime import datetime

STEAMSPY_ALL = "https://steamspy.com/api.php?request=all"
STORE_API_F = "https://store.steampowered.com/api/appdetails?appids={}&cc=us&l=en"
APPREV_F = "https://store.steampowered.com/appreviews/{appid}?json=1&filter=summary"

# ---------- Helper functions --------------------------------------------------

def owners_to_int(owner_str: str) -> int:
    """Convert SteamSpy owners string '20000 .. 50000' → upper bound as integer."""
    if not owner_str:
        return 0
    hi = owner_str.split(' .. ')[-1]
    return int(hi.replace(',', '')) if hi.isdigit() else 0

def get_game_pool(top_n: int) -> List[int]:
    """Fetch from SteamSpy 'all' and return a list of top_n appids sorted by owners descending."""
    data = requests.get(STEAMSPY_ALL, timeout=30).json()
    sorted_items = sorted(
        data.items(),
        key=lambda kv: owners_to_int(kv[1].get("owners", "")),
        reverse=True
    )
    return [int(appid) for appid, _ in sorted_items[:top_n]]

def parse_release_year(date_block: Dict[str, str]) -> Optional[int]:
    """Extract a 4-digit year from the 'date' field of Steam release_date."""
    raw = date_block.get("date", "")
    for token in raw.replace(',', '').split():
        if token.isdigit() and len(token) == 4:
            return int(token)
    return None

def parse_price(price_block: Optional[Dict[str, Any]]) -> float:
    """Convert Steam price_overview initial field (in cents) to USD float."""
    if not price_block:
        return 0.0
    return price_block.get("initial", 0) / 100

# ---------- Core fetching logic ------------------------------------------------

def fetch_store_data(appid: int) -> Optional[Dict[str, Any]]:
    """Fetch store metadata and review summary for a single appid."""
    try:
        store_json = requests.get(STORE_API_F.format(appid), timeout=20).json()
        blk = store_json.get(str(appid), {})
        if not blk.get("success"):
            return None
        info = blk["data"]
    except Exception as exc:
        print(f"[STORE] {appid} -> {exc}")
        return None

    # Review summary
    try:
        rev_json = requests.get(APPREV_F.format(appid=appid), timeout=20).json()
        summary = rev_json.get("query_summary", {})
        tot_reviews = summary.get("total_reviews", 0)
        tot_pos = summary.get("total_positive", 0)
        pos_ratio = round(tot_pos / tot_reviews, 4) if tot_reviews else None
    except Exception as exc:
        tot_reviews = tot_pos = pos_ratio = None
        print(f"[REV]   {appid} -> {exc}")

    return dict(
        appid             = appid,
        name              = info.get("name"),
        release_year      = parse_release_year(info.get("release_date", {})),
        price_usd         = parse_price(info.get("price_overview")),
        total_reviews     = tot_reviews,
        total_positive    = tot_pos,
        positive_ratio    = pos_ratio,
        genres            = "|".join(g["description"] for g in info.get("genres", [])),
        is_multiplayer    = int(any(cat.get("description") == "Multi-player"
                               for cat in info.get("categories", []))),
    )

def save_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    """Write rows to CSV at the given path; create directories if needed."""
    if not rows:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    keys = rows[0].keys()
    with open(path, "w", newline='', encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)

def crawl(top_n: int, out_path: str, sleep_sec: float, resume: bool):
    """
    Main crawl function:
    - If resume is True and out_path exists, skip appids already fetched.
    - Fetch top_n appids from SteamSpy, then for each:
      • Attempt up to 3 retries to get store data and review summary.
      • Sleep between requests to respect rate limiting.
    - Save all fetched rows to CSV. If resuming, append new rows to existing file.
    """
    # Track appids already fetched
    finished = set()
    if resume and os.path.isfile(out_path):
        with open(out_path, encoding="utf-8") as f:
            finished = {int(r["appid"]) for r in csv.DictReader(f)}
        print(f"Resume mode: {len(finished)} rows already in CSV, will skip them.")

    appids = [aid for aid in get_game_pool(top_n) if aid not in finished]
    total = len(appids)
    rows_accum: List[Dict[str, Any]] = []

    for idx, aid in enumerate(appids, 1):
        retries = 3
        details = None
        while retries and not details:
            details = fetch_store_data(aid)
            retries -= 1
            if not details:
                time.sleep(sleep_sec * 2)  # wait longer before retrying
        if details:
            rows_accum.append(details)

        # Progress display
        pct = (idx / total) * 100
        sys.stdout.write(f"\r{idx:4}/{total} fetched ({pct:5.1f}%)")
        sys.stdout.flush()
        time.sleep(sleep_sec)

    # If resuming, merge existing CSV rows with newly fetched rows
    if resume and os.path.isfile(out_path):
        with open(out_path, encoding="utf-8") as f:
            existing = list(csv.DictReader(f))
        rows_accum = existing + rows_accum

    save_csv(out_path, rows_accum)
    print(f"\n Saved {len(rows_accum)} rows → {out_path}")

# ---------- Command-line interface -------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Steam top games scraper (fetch ≥ 1000 rows).")
    parser.add_argument("-n", "--top_n", type=int, default=1000, help="Number of games to fetch")
    parser.add_argument("--sleep", type=float, default=0.3, help="Seconds to sleep between requests")
    parser.add_argument("--out", default="data/steam_games.csv", help="Output CSV path")
    parser.add_argument("--resume", action="store_true", help="If CSV exists, resume from where left off")
    args = parser.parse_args()

    crawl(args.top_n, args.out, args.sleep, args.resume)
