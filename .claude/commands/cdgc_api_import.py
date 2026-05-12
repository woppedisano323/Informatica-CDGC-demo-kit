import requests
import getpass
import time
import sys
import json
import subprocess
from pathlib import Path

LOGIN_URL  = "https://dmp-us.informaticacloud.com"
ORG_URL    = "https://idmc-api.dmp-us.informaticacloud.com"
IMPORT_DIR = Path.home() / "Downloads/CDGC_Import_RonkonkomaFinancial"

FILES_IN_ORDER = [
    "01_Domain.xlsx",
    "02_Subdomain.xlsx",
    "03_Regulation.xlsx",
    "04_Policy.xlsx",
    "05_Legal_Entity.xlsx",
    "06_Business_Area.xlsx",
    "07_Geography.xlsx",
    "08_System.xlsx",
    "09_AI_System.xlsx",
    "10_AI_Model.xlsx",
    "11_Business_Term.xlsx",
    "12_Data_Set.xlsx",
    "13_DQ_Rule_Template.xlsx",
    "14_Relationships.xlsx",
]

def authenticate(username, password):
    resp = requests.post(
        f"{LOGIN_URL}/identity-service/api/v1/Login",
        json={"username": username, "password": password},
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    session_id = data["sessionId"]
    org_id = data["orgId"]

    resp = requests.get(
        f"{LOGIN_URL}/identity-service/api/v1/jwt/Token?client_id=idmc_api&nonce=1234",
        headers={"IDS-SESSION-ID": session_id},
        cookies={"USER_SESSION": session_id},
        timeout=30
    )
    resp.raise_for_status()
    token_data = resp.json()
    jwt_token = token_data.get("token") or token_data.get("jwt_token") or token_data.get("access_token")
    print(f"  ✓ Authenticated — orgId: {org_id}")
    return jwt_token, org_id

def import_file(jwt_token, org_id, filepath):
    cmd = [
        "curl", "-s", "-X", "POST",
        f"{ORG_URL}/data360/content/import/v1/assets",
        "-H", f"Authorization: Bearer {jwt_token}",
        "-H", f"X-INFA-ORG-ID: {org_id}",
        "-F", f"file=@{filepath}",
        "-F", 'config={"validationPolicy": "CONTINUE_ON_ERROR_WARNING"};type=application/json'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        return None, f"curl error: {result.stderr[:200]}"
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None, f"Invalid response: {result.stdout[:200]}"
    if "error" in data or "errorMessage" in data:
        if "401" in str(data):
            return None, "401"
        return None, f"API error: {result.stdout[:300]}"
    if data.get("jobId"):
        return data["jobId"], None
    return None, f"No jobId in response: {result.stdout[:300]}"

def poll_job(jwt_token, org_id, job_id, filename):
    url = f"{ORG_URL}/data360/observable/v1/jobs/{job_id}"
    headers = {"Authorization": f"Bearer {jwt_token}", "X-INFA-ORG-ID": org_id}
    terminal = {"COMPLETED", "FAILED", "COMPLETED_WITH_ERRORS"}
    dots = 0
    while True:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        status = resp.json().get("status", "UNKNOWN")
        if status in terminal:
            print(f"\r  [{filename}] {status}          ")
            return status, resp.json()
        print(f"\r  [{filename}] {status}{'.' * (dots % 4)}   ", end="", flush=True)
        dots += 1
        time.sleep(5)

# ── Main ──────────────────────────────────────────────────────────────────────

print("\nCDGC API Import")
print("───────────────────────────────────────────")
username = input("IDMC Username: ")
password = getpass.getpass("IDMC Password: ")

print("\nAuthenticating...")
jwt_token, org_id = authenticate(username, password)

results = []
for fname in FILES_IN_ORDER:
    fpath = IMPORT_DIR / fname
    if not fpath.exists():
        print(f"\nSKIP — file not found: {fpath}")
        results.append((fname, "SKIPPED"))
        continue

    print(f"\nImporting {fname}...")
    job_id, err = import_file(jwt_token, org_id, fpath)

    if err == "401":
        print("  Token expired — re-authenticating...")
        jwt_token, org_id = authenticate(username, password)
        job_id, err = import_file(jwt_token, org_id, fpath)

    if err:
        print(f"  FAILED to submit: {err}")
        results.append((fname, "SUBMIT_FAILED"))
        print(f"\nFATAL — stopping import. Fix {fname} and retry.")
        sys.exit(1)

    status, detail = poll_job(jwt_token, org_id, job_id, fname)
    results.append((fname, status))

    if status == "FAILED":
        print(f"\nFATAL — {fname} failed. Stopping import.")
        print(detail)
        sys.exit(1)

print("\n── Import Summary ──────────────────────────────────────────")
for fname, status in results:
    icon = "✓" if status == "COMPLETED" else "⚠" if status == "COMPLETED_WITH_ERRORS" else "✗"
    print(f"  {icon}  {fname:<45} {status}")
print("────────────────────────────────────────────────────────────\n")
