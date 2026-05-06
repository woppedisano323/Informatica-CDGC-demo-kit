"""
CDGC Business Glossary Loader
Reads glossary terms from CSV and loads them into Informatica CDGC via REST API.

Usage:
    python3 cdgc_glossary_loader.py \
        --username your@email.com \
        --password yourpassword \
        --org-url https://<your-org>.informaticacloud.com

Optional flags:
    --csv       Path to glossary CSV (default: CDGC_Glossary_Import.csv)
    --dry-run   Print payloads without calling the API
    --category  Only load terms for a specific category

Note: Find your org URL in IDMC → Administrator → Organization → Pod URL.
"""

import argparse
import csv
import json
import sys
import requests
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

LOGIN_URL   = "https://dm-us.informaticacloud.com/ma/api/v2/user/login"

# CDGC REST API paths — verify these against your org's API explorer if needed
# Navigator: IDMC → Administrator → API Documentation (if enabled)
CATEGORY_PATH = "/ccgf-dataasset-api/api/v2/glossary/categories"
TERM_PATH     = "/ccgf-dataasset-api/api/v2/glossary/businessTerms"

DEFAULT_CSV   = Path(__file__).parent / "CDGC_Glossary_Import.csv"

# ── Auth ──────────────────────────────────────────────────────────────────────

def login(username: str, password: str) -> dict:
    payload = {
        "@type": "login",
        "username": username,
        "password": password
    }
    resp = requests.post(LOGIN_URL, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    session_id = data.get("sessionId") or data.get("icSessionId")
    if not session_id:
        print("ERROR: No sessionId in login response. Check credentials.")
        print(json.dumps(data, indent=2))
        sys.exit(1)
    print(f"✓ Authenticated as {username}")
    return {"sessionId": session_id}


def headers(session_id: str) -> dict:
    return {
        "Content-Type": "application/json",
        "INFA-SESSION-ID": session_id
    }

# ── Category management ───────────────────────────────────────────────────────

def get_existing_categories(org_url: str, session_id: str) -> dict:
    url = org_url + CATEGORY_PATH
    resp = requests.get(url, headers=headers(session_id), timeout=30)
    if resp.status_code == 404:
        print("WARN: Category endpoint not found — check CATEGORY_PATH in config.")
        return {}
    resp.raise_for_status()
    cats = {}
    for item in resp.json().get("items", resp.json() if isinstance(resp.json(), list) else []):
        cats[item.get("name", "")] = item.get("id", "")
    return cats


def create_category(org_url: str, session_id: str, name: str, dry_run: bool) -> str:
    payload = {"name": name, "description": f"Business glossary category for {name}"}
    if dry_run:
        print(f"  [DRY RUN] POST {CATEGORY_PATH} → {json.dumps(payload)}")
        return f"dry-run-id-{name.replace(' ', '-').lower()}"
    url = org_url + CATEGORY_PATH
    resp = requests.post(url, headers=headers(session_id), json=payload, timeout=30)
    if resp.status_code in (200, 201):
        cat_id = resp.json().get("id", "")
        print(f"  ✓ Created category: {name} (id: {cat_id})")
        return cat_id
    print(f"  ✗ Failed to create category '{name}': {resp.status_code} {resp.text[:200]}")
    return ""

# ── Term management ───────────────────────────────────────────────────────────

def build_term_payload(row: dict, category_id: str) -> dict:
    payload = {
        "name": row["Name"].strip(),
        "description": row["Description"].strip(),
        "status": row.get("Status", "Draft").strip(),
        "categoryId": category_id,
    }
    if row.get("Abbreviation", "").strip():
        payload["abbreviation"] = row["Abbreviation"].strip()
    if row.get("Synonyms", "").strip():
        payload["synonyms"] = [s.strip() for s in row["Synonyms"].split(",") if s.strip()]
    if row.get("Steward Notes", "").strip():
        payload["additionalInformation"] = row["Steward Notes"].strip()
    return payload


def create_term(org_url: str, session_id: str, payload: dict, dry_run: bool) -> bool:
    if dry_run:
        print(f"  [DRY RUN] POST {TERM_PATH} → name='{payload['name']}'")
        return True
    url = org_url + TERM_PATH
    resp = requests.post(url, headers=headers(session_id), json=payload, timeout=30)
    if resp.status_code in (200, 201):
        print(f"  ✓ Created term: {payload['name']}")
        return True
    if resp.status_code == 409:
        print(f"  ~ Skipped (already exists): {payload['name']}")
        return True
    print(f"  ✗ Failed '{payload['name']}': {resp.status_code} {resp.text[:200]}")
    return False

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Load CDGC glossary from CSV")
    parser.add_argument("--username",  required=True, help="IDMC username (email)")
    parser.add_argument("--password",  required=True, help="IDMC password")
    parser.add_argument("--org-url",   required=True, help="Your IDMC org base URL (e.g. https://usw1.dmp-us.informaticacloud.com)")
    parser.add_argument("--csv",       default=str(DEFAULT_CSV), help="Path to glossary CSV")
    parser.add_argument("--dry-run",   action="store_true", help="Print payloads without calling API")
    parser.add_argument("--category",  help="Only load terms for this category")
    args = parser.parse_args()

    org_url = args.org_url.rstrip("/")

    # Read CSV
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"ERROR: CSV not found at {csv_path}")
        sys.exit(1)

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"✓ Loaded {len(rows)} terms from {csv_path.name}")

    # Filter by category if specified
    if args.category:
        rows = [r for r in rows if r["Category"].strip().lower() == args.category.lower()]
        print(f"✓ Filtered to {len(rows)} terms in category '{args.category}'")

    # Authenticate
    if args.dry_run:
        session_id = "dry-run-session"
        print("✓ Dry-run mode — no API calls will be made")
    else:
        session = login(args.username, args.password)
        session_id = session["sessionId"]

    # Get existing categories
    existing_categories = {} if args.dry_run else get_existing_categories(org_url, session_id)

    # Group rows by category
    categories = {}
    for row in rows:
        cat = row["Category"].strip()
        categories.setdefault(cat, []).append(row)

    # Process each category
    results = {"created": 0, "skipped": 0, "failed": 0}

    for cat_name, terms in categories.items():
        print(f"\n── Category: {cat_name} ({len(terms)} terms) ──")

        cat_id = existing_categories.get(cat_name, "")
        if not cat_id:
            cat_id = create_category(org_url, session_id, cat_name, args.dry_run)
        else:
            print(f"  ~ Category exists (id: {cat_id})")

        if not cat_id:
            print(f"  ✗ Skipping all terms — could not get/create category")
            results["failed"] += len(terms)
            continue

        for row in terms:
            payload = build_term_payload(row, cat_id)
            success = create_term(org_url, session_id, payload, args.dry_run)
            if success:
                results["created"] += 1
            else:
                results["failed"] += 1

    print(f"\n{'='*50}")
    print(f"Complete — Created: {results['created']} | Failed: {results['failed']}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
