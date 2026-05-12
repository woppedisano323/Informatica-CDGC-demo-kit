import requests
import getpass
import sys
import time

LOGIN_URL = "https://dmp-us.informaticacloud.com"
ORG_URL   = "https://idmc-api.dmp-us.informaticacloud.com"

# classType search works for all types EXCEPT AIModel and AISystem on this org —
# those are deleted by scanning all externalIds with known prefixes instead
SEARCH_TYPES = [
    ("DQ Rule Templates", "com.infa.ccgf.models.governance.RuleTemplate"),
    ("Business Terms",    "com.infa.ccgf.models.governance.BusinessTerm"),
    ("Data Sets",         "com.infa.ccgf.models.governance.DataSet"),
    ("Systems",           "com.infa.ccgf.models.governance.System"),
    ("Business Areas",    "com.infa.ccgf.models.governance.BusinessArea"),
    ("Legal Entities",    "com.infa.ccgf.models.governance.LegalEntity"),
    ("Geographies",       "com.infa.ccgf.models.governance.Geography"),
    ("Policies",          "com.infa.ccgf.models.governance.Policy"),
    ("Regulations",       "com.infa.ccgf.models.governance.Regulation"),
    ("Subdomains",        "com.infa.ccgf.models.governance.Subdomain"),
    ("Domains",           "com.infa.ccgf.models.governance.Domain"),
]

username        = input("IDMC Username: ")
password        = getpass.getpass("IDMC Password: ")
customer_prefix = input("Customer prefix (e.g. RKF for Ronkonkoma): ").strip().upper()

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

def delete_one(ext_id):
    r = requests.delete(
        f"{ORG_URL}/data360/content/v1/assets/{ext_id}?scheme=external",
        headers=h_d, timeout=30)
    if r.status_code == 429:
        time.sleep(15)
        r = requests.delete(
            f"{ORG_URL}/data360/content/v1/assets/{ext_id}?scheme=external",
            headers=h_d, timeout=30)
    return r.status_code in (200, 201, 204, 404)

def search_type(class_type):
    for attempt in range(3):
        r = requests.post(
            f"{ORG_URL}/data360/search/v1/assets?knowledgeQuery=*&segments=summary",
            headers=h_s,
            json={"from": 0, "size": 100,
                  "filterSpec": [{"type": "simple", "attribute": "core.classType", "values": [class_type]}]},
            timeout=30)
        if r.status_code == 429:
            time.sleep(15)
            continue
        if not r.text.strip():
            time.sleep(3)
            continue
        try:
            return r.json().get("hits", [])
        except Exception:
            time.sleep(3)
    return []

# ── Scan ──────────────────────────────────────────────────────────────────────

# AI Models and AI Systems: probe by externalId — classType search returns 0 on suborg
print("Scanning for AI Models and AI Systems by externalId probe...")
ai_to_delete = []
for suffix, label in [("AIM", "AI Model"), ("AIS", "AI System")]:
    found = []
    for i in range(1, 30):
        ext_id = f"{customer_prefix}{suffix}-{i}"
        r = requests.delete(
            f"{ORG_URL}/data360/content/v1/assets/{ext_id}?scheme=external",
            headers=h_d, timeout=30)
        if r.status_code == 404:
            break  # no more in sequence
        if r.status_code in (200, 201, 204):
            found.append(ext_id)
        time.sleep(0.2)
    print(f"  {label+'s':<25}: {len(found)} {'(deleted during probe)' if found else ''}")
    ai_to_delete.extend(found)

# All other types via classType search
all_assets = {}
total_search = 0
for label, class_type in SEARCH_TYPES:
    hits = search_type(class_type)
    all_assets[label] = hits
    total_search += len(hits)
    print(f"  {label:<25}: {len(hits)}")
    time.sleep(0.5)

total = total_search  # AI assets already deleted during probe above
print(f"\n  {'Total (search)':<25}: {total}")

if total == 0 and not ai_to_delete:
    print("\nOrg is clean — nothing to delete.")
    sys.exit(0)

confirm = input(f"\n⚠ This will permanently delete all remaining {total} assets.\n  Type CONFIRM to proceed: ")
if confirm.strip() != "CONFIRM":
    print("Cancelled.")
    sys.exit(0)

# ── Delete remaining search assets ────────────────────────────────────────────
total_cleared = 0
total_failed  = 0
print()
for label, class_type in SEARCH_TYPES:
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
        ok = delete_one(ext_id)
        if ok:
            print(f"    ✓ {name!r}")
            total_cleared += 1
        else:
            print(f"    ✗ {name!r} — unexpected response, delete manually in UI")
            total_failed += 1
        time.sleep(0.5)

print(f"\nCleared: {total_cleared + len(ai_to_delete)}  |  Failed: {total_failed}")
if total_failed:
    print("Failed assets may need manual deletion in the CDGC UI.")

# ── Second pass — catch any stragglers missed in first pass ──────────────────
print("\nRunning second pass for stragglers...")
time.sleep(3)
straggler_cleared = 0
for label, class_type in SEARCH_TYPES:
    hits = search_type(class_type)
    if not hits:
        continue
    print(f"  {label}: {len(hits)} remaining")
    for item in hits:
        ext_id = item.get("core.externalId", "")
        name   = (item.get("summary") or {}).get("core.name", "?")
        if not ext_id:
            print(f"    ✗ {name!r} — no externalId, delete manually in UI")
            continue
        ok = delete_one(ext_id)
        if ok:
            print(f"    ✓ {name!r}")
            straggler_cleared += 1
        time.sleep(0.5)
if straggler_cleared:
    print(f"  Second pass cleared {straggler_cleared} additional assets.")
    time.sleep(3)

# ── Final verification scan ───────────────────────────────────────────────────
print("\nVerifying org is clean...\n")
time.sleep(3)  # brief pause for async deletion to settle
grand_total = 0
ALL_TYPES = SEARCH_TYPES + [
    ("AI Models",  "com.infa.ccgf.models.governance.AIModel"),
    ("AI Systems", "com.infa.ccgf.models.governance.AISystem"),
]
for label, class_type in ALL_TYPES:
    hits = search_type(class_type)
    count = len(hits)
    grand_total += count
    status = "✓" if count == 0 else "⚠"
    print(f"  {status} {label:<25}: {count}")

print(f"\n  {'Total':<25}: {grand_total}")
if grand_total == 0:
    print("\nOrg is clean — ready for import.")
else:
    print("\n⚠ Some assets remain. Check the CDGC UI and re-run if needed.")
