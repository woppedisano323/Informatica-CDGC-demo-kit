---
description: Wipe all governance assets from a CDGC org — Domains, Subdomains, Business Terms, Policies, Regulations, Systems, AI Systems, AI Models, Data Sets, Business Areas, Legal Entities, Geographies, DQ Rule Templates. Use before reloading a demo environment. Requires API credentials. Prompts for confirmation before deleting anything.
---

# CDGC Glossary Wipe

You are an Informatica CDGC specialist. This skill deletes all governance assets from a CDGC org to prepare it for a clean demo reload. It is destructive and irreversible — always confirm with the user before executing.

---

## Overview

This skill:
1. Authenticates to IDMC using the two-step JWT flow
2. Searches for all governance assets by type
3. Presents a count summary and asks for explicit confirmation
4. Deletes assets in reverse dependency order using `DELETE /data360/content/v1/assets/{externalId}?scheme=external`
5. Loops until 404 confirms each asset is fully gone
6. Reports a final summary of what was deleted

### Key facts about the delete endpoint

The bulk import `Operation=Delete` approach does not work on suborg accounts — import jobs FAIL silently. The working approach is:

```
DELETE {ORG_URL}/data360/content/v1/assets/{externalId}?scheme=external
```

- Use `core.externalId` (e.g., `BT-3`, `DOM-1`) — NOT `core.identity` (UUID)
- Returns HTTP 201 + `{"messageCode":"Asset with id: [X] deleted"}` on success
- Loop the delete until 404 is returned — confirms the asset is fully gone
- UUID-based delete (`DELETE /assets/{uuid}`) returns 404 — not supported for governance assets
- 429 rate limit: sleep 15s and retry

### Deletion order

Order matters — dependency relationships block deletion if parents are deleted before children:

1. DQ Rule Templates — their glossary links block Business Term deletion
2. Business Terms
3. Data Sets
4. AI Models — must come before AI Systems (AI Model has AI System as parent)
5. AI Systems
6. Systems
7. Business Areas
8. Legal Entities
9. Geographies
10. Policies
11. Regulations
12. **Subdomains** — must come before Domains (auto-relationship blocks Domain deletion)
13. **Domains** — last

### Confirmed classTypes (tested and verified)

```
com.infa.ccgf.models.governance.RuleTemplate       ← DQ Rule Template (NOT DataQualityRuleTemplate)
com.infa.ccgf.models.governance.BusinessTerm
com.infa.ccgf.models.governance.DataSet
com.infa.ccgf.models.governance.AIModel
com.infa.ccgf.models.governance.AISystem
com.infa.ccgf.models.governance.System
com.infa.ccgf.models.governance.BusinessArea
com.infa.ccgf.models.governance.LegalEntity
com.infa.ccgf.models.governance.Geography
com.infa.ccgf.models.governance.Policy
com.infa.ccgf.models.governance.Regulation
com.infa.ccgf.models.governance.Subdomain          ← NOT SubjectArea
com.infa.ccgf.models.governance.Domain
```

---

## Step 0 — Warn and collect credentials

Present this warning before collecting anything:

```
╔══════════════════════════════════════════════════════════════════╗
║              ⚠  DESTRUCTIVE OPERATION — READ CAREFULLY           ║
╚══════════════════════════════════════════════════════════════════╝

This process will PERMANENTLY WIPE your CDGC implementation.

All governance assets will be deleted — this includes:
  • All Domains and Subdomains
  • All Business Terms
  • All Policies and Regulations
  • All Systems, AI Systems, AI Models, Data Sets, Business Areas, Legal Entities, and Geographies
  • All DQ Rule Templates

There is NO undo. Deleted assets cannot be recovered from the UI
or the API. If you need a backup, export your assets first.

This skill is intended for sandbox and demo orgs only.
DO NOT run this against a production environment.

If you are sure you want to continue, provide your IDMC credentials
below. They are used only in this session to generate a temporary
JWT token and are not stored anywhere.
```

Collect:
- `USERNAME` — IDMC username (not necessarily an email address)
- `PASSWORD` — IDMC password (use getpass — never print)

---

## Step 1 — Write and execute the wipe script

Use this exact script — it is tested and verified:

```python
import requests
import getpass
import sys
import time

LOGIN_URL = "https://dmp-us.informaticacloud.com"
ORG_URL   = "https://idmc-api.dmp-us.informaticacloud.com"

ASSET_TYPES = [
    ("DQ Rule Templates", "com.infa.ccgf.models.governance.RuleTemplate"),
    ("Business Terms",    "com.infa.ccgf.models.governance.BusinessTerm"),
    ("Data Sets",         "com.infa.ccgf.models.governance.DataSet"),
    ("AI Models",         "com.infa.ccgf.models.governance.AIModel"),
    ("AI Systems",        "com.infa.ccgf.models.governance.AISystem"),
    ("Systems",           "com.infa.ccgf.models.governance.System"),
    ("Business Areas",    "com.infa.ccgf.models.governance.BusinessArea"),
    ("Legal Entities",    "com.infa.ccgf.models.governance.LegalEntity"),
    ("Geographies",       "com.infa.ccgf.models.governance.Geography"),
    ("Policies",          "com.infa.ccgf.models.governance.Policy"),
    ("Regulations",       "com.infa.ccgf.models.governance.Regulation"),
    ("Subdomains",        "com.infa.ccgf.models.governance.Subdomain"),
    ("Domains",           "com.infa.ccgf.models.governance.Domain"),
]

username = input("IDMC Username: ")
password = getpass.getpass("IDMC Password: ")

resp = requests.post(f"{LOGIN_URL}/identity-service/api/v1/Login",
    json={"username": username, "password": password}, timeout=30)
resp.raise_for_status()
data = resp.json()
session_id = data["sessionId"]
org_id = data["orgId"]
resp = requests.get(
    f"{LOGIN_URL}/identity-service/api/v1/jwt/Token?client_id=idmc_api&nonce=1234",
    headers={"IDS-SESSION-ID": session_id},
    cookies={"USER_SESSION": session_id}, timeout=30)
resp.raise_for_status()
jwt = resp.json().get("token") or resp.json().get("jwt_token") or resp.json().get("access_token")
print(f"✓ Authenticated\n")

h_s = {"Authorization": f"Bearer {jwt}", "X-INFA-ORG-ID": org_id, "Content-Type": "application/json"}
h_d = {"Authorization": f"Bearer {jwt}", "X-INFA-ORG-ID": org_id}

def delete_until_gone(ext_id):
    """Loop DELETE until 404 confirms fully gone."""
    for attempt in range(1, 20):
        r = requests.delete(
            f"{ORG_URL}/data360/content/v1/assets/{ext_id}?scheme=external",
            headers=h_d, timeout=30)
        if r.status_code == 429:
            print(f"      rate limited, waiting 15s...")
            time.sleep(15)
            continue
        try:
            body = r.json()
        except Exception:
            body = {}
        msg = body.get("messageCode", r.text[:80])
        if r.status_code == 404 or "not found" in str(msg).lower():
            return True   # confirmed gone
        if "deleted" in str(msg).lower() or r.status_code in (200, 201, 204):
            time.sleep(0.5)
            continue      # deleted one copy, loop to clear duplicates
        return False      # unexpected response
    return False

# Scan
total = 0
all_assets = {}
for label, class_type in ASSET_TYPES:
    r = requests.post(
        f"{ORG_URL}/data360/search/v1/assets?knowledgeQuery=*&segments=summary",
        headers=h_s,
        json={"from": 0, "size": 100,
              "filterSpec": [{"type": "simple", "attribute": "core.classType", "values": [class_type]}]},
        timeout=30)
    hits = r.json().get("hits", [])
    all_assets[label] = hits
    total += len(hits)
    print(f"  {label:<25}: {len(hits)}")

print(f"\n  {'Total':<25}: {total}")
if total == 0:
    print("\nOrg is clean — nothing to delete.")
    sys.exit(0)

confirm = input(f"\n⚠ This will permanently delete all {total} assets.\n  Type CONFIRM to proceed: ")
if confirm.strip() != "CONFIRM":
    print("Cancelled.")
    sys.exit(0)

# Delete
total_cleared = 0
total_failed  = 0
print()
for label, class_type in ASSET_TYPES:
    hits = all_assets[label]
    if not hits:
        continue
    print(f"  {label}: {len(hits)} found")
    for item in hits:
        name   = (item.get("summary") or {}).get("core.name", "?")
        ext_id = item.get("core.externalId", "")
        if not ext_id:
            print(f"    ✗ {name!r} — no externalId, delete manually in UI")
            total_failed += 1
            continue
        ok = delete_until_gone(ext_id)
        if ok:
            print(f"    ✓ {name!r}")
            total_cleared += 1
        else:
            print(f"    ✗ {name!r} — unexpected response, delete manually in UI")
            total_failed += 1
        time.sleep(0.5)

print(f"\nCleared: {total_cleared}  |  Failed: {total_failed}")
if total_failed:
    print("Failed assets may need manual deletion in the CDGC UI.")
if total_cleared == 0 and total_failed == 0:
    print("Nothing found — org is clean.")
```

---

## Safety rules

- **Never run against a production org** — always confirm the org URL before proceeding
- **Confirmation is mandatory** — the script will not delete anything without the user typing `CONFIRM`
- **No undo** — deleted assets cannot be recovered; export first if you need a backup
- **If the UI still shows assets after the wipe completes** — run `cdgc_scan.py` to verify via the API. If scan shows 0, the org is clean. The UI is not authoritative — the scan is.

---

## Sharing this skill

Copy `cdgc-wipe.md` to `~/.claude/commands/cdgc-wipe.md`.
Invoke with `/cdgc-wipe` in any Claude Code session.
