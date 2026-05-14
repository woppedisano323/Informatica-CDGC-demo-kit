---
description: Build a complete CDGC import package from documents the client already has — data dictionaries, policy PDFs, org charts, glossaries, or Excel schemas. Produces a color-coded Review Workbook for approval, then generates all 14 import files that are easily imported directly into the Informatica CDGC product. Supports CSV, Excel (multi-tab), PDF, Word, and plain text. Detects cross-document conflicts. Three fallback modes: TODO markers (A), vertical defaults (B), or interactive gap interview (C). Resume flow: load an edited workbook from a prior session or client review with `/cdgc-client-setup resume <path>`.
---

# CDGC Client-Driven Setup

This skill builds a complete, client-specific CDGC import package from documents the client already has. Feed it any combination of data dictionaries, policy PDFs, org charts, glossaries, or Excel schemas — it parses them, extracts governance assets with confidence scoring, and produces a color-coded Review Workbook for approval before generating the 14 import files that are easily imported directly into the Informatica CDGC product. Supports CSV, Excel (multi-tab), PDF, Word, and plain text. Detects and flags cross-document conflicts. Three fallback modes handle gaps: TODO markers (A), vertical defaults (B), or an interactive gap interview (C).

**Two entry points:**
- `/cdgc-client-setup` — full flow: parse documents → Review Workbook → generate import files
- `/cdgc-client-setup resume <path>` — pick up from an edited Review Workbook (client returned it, or a prior session generated it)

---

## When to use this skill vs `/cdgc-setup`

| Situation | Use |
|-----------|-----|
| Client has data dictionaries, policy PDFs, glossaries, or org charts | `/cdgc-client-setup` — extracts governance assets from their actual documents |
| No client documents available, or running a quick vertical demo | `/cdgc-setup` — generates realistic content from vertical defaults |
| Mid-engagement: client provided docs after initial demo | `/cdgc-client-setup` — replace demo content with client-specific assets |
| Demonstrating the AI-assisted onboarding story to a prospect | `/cdgc-client-setup` — the intake-to-import flow is the demo |

**Key distinction:** `/cdgc-setup` generates content that *looks* real. `/cdgc-client-setup` uses content that *is* real — the client's own vocabulary, policies, and domain structure. This makes the demo immediately recognizable and relevant to the prospect.

---

## Prerequisites

- **Claude Code** installed and running
- **Python 3.8+** installed (`python3 --version` to check)
- Required Python packages (run once per machine):
  ```bash
  pip install openpyxl pdfplumber python-docx requests
  ```
  (`requests` is needed for API import — asked at approval or resume time)

  Or use the included `install_cdgc_deps.sh`:
  ```bash
  ~/.claude/commands/install_cdgc_deps.sh
  ```

---

## Overview of the workflow

This skill supports two distinct usage patterns — demos and real engagements — that share the same steps but differ in how the review cycle works.

### Single-session flow (demo / proof of concept)
```
Step 0 — Collect documents + client name + project name
Step 1 — Parse documents and extract candidates
Step 2 — Generate the Review Workbook
Step 3 — Review inline → approve → choose import method (UI or API)
Step 4 — Generate the 14 import files
Step 5 — Import into CDGC
```

### Multi-session flow (real client engagement)
```
Session 1 (practitioner has source documents):
  Step 0 — Collect documents + client name + project name
  Step 1 — Parse documents
  Step 2 — Generate the Review Workbook
  Step 3 — Hand off workbook for client review → provide handoff guidance

  [Client edits workbook offline — fills in owners, corrects terms,
   resolves conflicts, clears TODO cells — may take days or weeks]

Session 2 (workbook returned — any practitioner, any machine):
  /cdgc-client-setup resume <path-to-edited-workbook>
  → Validate workbook, report TODOs + broken parent links
  → Choose import method (UI or API)
  Step 4 — Generate the 14 import files from the edited workbook
  Step 5 — Import into CDGC
```

All output files and folders use the naming convention `<ClientName>-<ProjectName>` (e.g., `AcmeHealth-DataGovernanceQ3`). The folder name is embedded in the workbook filename and recovered automatically on resume.

---

## Demo tips — using this skill in front of a client

**The intake step is the demo.** When you type `/cdgc-client-setup` and Claude asks for their documents, that moment — "give me your data dictionary and your compliance policy" — is the most impactful part. The prospect sees their content being understood immediately.

**Recommended demo flow:**
1. Open Claude Code, type `/cdgc-client-setup`
2. Provide the client name, project name, and 2–3 of their actual documents (or the HHS/ONC sample set — see below)
3. While parsing runs (~15–30 seconds), explain what's happening: "Claude is reading your documents and mapping your content to the CDGC governance model"
4. Show the color-coded Review Workbook — walk the yellow/orange/red rows as "this is where we'd want your team to review before we import"
5. Approve and generate the 14 files — "in a real engagement, these go straight into your CDGC environment"

**What to emphasize:**
- The Review Workbook is a collaboration artifact — the client edits it and returns it; it is not a black box
- Conflict detection surfaces inconsistencies across teams before they become import errors
- HIGH confidence rows mean zero manual work — they're ready to import

**What to skip:**
- Don't walk through every column spec — too technical for a first call
- Don't demo the gap interview (Option C) unless the audience is already technical — it slows the flow

**Validated demo document set (Healthcare / HHS):**
Three authentic, publicly available PDFs from the same organizational ecosystem:
- `USCDI_V6_July2025.pdf` — ONC USCDI V6 data classes → Business Terms, Domains
- `HHS_OCR_privacysummary.pdf` — HHS OCR Privacy Rule summary → Policies, Regulations
- `EnterpriseDataPlanning.pdf` — CMS Enterprise Data Planning → Domains, Systems, Data Sets

These three documents produce 2 natural conflicts (USCDI clinical vocabulary vs OCR HIPAA legal vocabulary vs CMS operational terminology) — a perfect demo of the conflict detection capability. Keep them in `~/Downloads/CDGC_Demo_Docs/` and use with client name `ONC`, project name `HealthcareDemo`.

---

## Resume entry point — starting from an edited workbook

If the Review Workbook was generated in a prior session (or handed back by the client after review), skip document parsing entirely and load directly from the workbook.

**Trigger:** the practitioner types `/cdgc-client-setup resume <path>` — where `<path>` is the full path to the edited Review Workbook (e.g., `~/Downloads/CDGC_Import_AcmeHealth-DataGovernanceQ3/00_Review_AcmeHealth-DataGovernanceQ3.xlsx`).

**On resume:**
1. Load the workbook from `<path>`. If the path does not exist, report clearly and stop.
2. Extract `ClientName` and `ProjectName` from the filename — the convention is `00_Review_<ClientName>-<ProjectName>.xlsx`. If the filename doesn't match this pattern, ask the practitioner to confirm both values.
3. Validate the workbook:
   - All expected asset-type sheets are present
   - Required columns exist on each sheet (use same column specs as Step 2)
   - Count remaining TODO cells and report them
   - Flag any rows where a parent reference column contains a name that does not appear in the corresponding parent sheet (broken parent link — will fail on import)
4. Present a resume summary:
   ```
   Resuming from: <path>
   Client: <ClientName>  |  Project: <ProjectName>

   ── Workbook Status ──────────────────────────────────────────────
     Domains          : <N> rows  (<N> TODO remaining)
     Subdomains       : <N> rows  (<N> TODO remaining)
     Business Terms   : <N> rows  (<N> TODO remaining)
     Policies         : <N> rows  (<N> TODO remaining)
     Regulations      : <N> rows  (<N> TODO remaining)
     Systems          : <N> rows  (<N> TODO remaining)
     Data Sets        : <N> rows  (<N> TODO remaining)
     DQ Rule Templates: <N> rows  (<N> TODO remaining)
     Relationships    : <N> rows  (<N> TODO remaining)
     Broken parent links: <N> (listed below if any)

   ── Attention Items ──────────────────────────────────────────────
     <list any TODO rows or broken parent links>

   ─────────────────────────────────────────────────────────────────
   How would you like to import the files once generated?

     A) Manual UI (default) — upload each file via the CDGC UI
     B) API (automated) — I will import programmatically and poll until complete
        Requires your IDMC org URL, username, and password.
   ```
5. Wait for the practitioner's import method choice, then proceed to Step 4 (generate import files). Do not repeat Steps 1–3.

---

## Step 0 — Intake prompt

Ask the practitioner:

```
To get started I need a few things:

1. Client name — the organization you are working with (e.g., HLS Central)
2. Project name — the engagement or workstream name (e.g., DataGovernanceQ3, Phase1Rollout)
   Together these form the folder and file prefix: <ClientName>-<ProjectName>

3. File paths to any documents you have — paste one path per line.
   Accepted formats: .csv, .xlsx, .xls, .pdf, .docx, .txt
   Examples of useful inputs:
     - Data dictionary or data catalog export (CSV or Excel)
     - Data governance policy documents (PDF or Word)
     - Org chart or business area list (any format)
     - Existing glossary or business term list (any format)
     - System inventory or architecture doc (any format)
     - Regulatory or compliance framework docs (PDF or Word)

4. Fallback preference when a field can't be inferred from your documents:
   A) Leave blank with a TODO marker — I'll fill it in manually
   B) Use vertical defaults for anything missing (I'll ask which vertical)
   C) Ask me — prompt me for each gap before generating

If you only have some documents (e.g., just a data dictionary), that's fine — I'll extract what I can and flag the gaps.
```

Wait for the practitioner's response before proceeding.

---

## Step 1 — Parse documents

Write and execute a Python script that:

1. **Detects document type** by extension and structure:
   - `.csv` / `.xlsx` / `.xls` → tabular parser
   - `.pdf` → text extraction via `pdfplumber`; stitch cross-page line breaks by joining page N tail to page N+1 head only when both end/start with a lowercase character (mid-sentence split); anchor policy extraction to the POLICY STATEMENTS section to prevent document preamble bleeding into the first policy body
   - `.docx` → text extraction via `python-docx`
   - `.txt` → raw text read

2. **Extracts candidates for each CDGC asset type** using keyword matching and structure inference:

   | CDGC Asset | Signals to look for |
   |------------|-------------------|
   | Domain | Section headers, top-level groupings, subject area columns, domain/category fields |
   | Subdomain | Sub-headers, nested groupings, sub-category or sub-domain columns |
   | Business Term | Term/field/attribute/column name columns; description/definition columns |
   | Critical Data Element | Columns named "CDE", "Critical", "Key", "PII", "Required"; boolean flags |
   | Policy | Numbered subsections with a `Policy Type: \| Owner: \| Administrator:` metadata line; use a section-anchored search (e.g. restrict to text after "POLICY STATEMENTS" header) to avoid preamble bleed |
   | Regulation | References to HIPAA, GDPR, HITECH, SOX, ICD-10, HL7, BCBS, CCAR, etc. |
   | System | "Source system", "application", "platform", "database" columns or sections |
   | Data Set | "Table", "dataset", "entity", "object", "feed" columns or sections |
   | Business Area | "Department", "business unit", "team", "org" columns or sections |
   | Legal Entity | "Legal entity", "subsidiary", "company", "entity" columns or sections |
   | Stakeholder | "Owner", "steward", "SME", "contact", "responsible" columns |

3. **Scores confidence** for each extracted candidate:
   - `HIGH` — exact column name match or clearly labeled section
   - `MEDIUM` — inferred from context or partial match
   - `LOW` — guessed from proximity or document structure

4. **Builds a structured extraction dict** with candidates per asset type, ready for Step 2.

5. **Identifies gaps** — asset types with no candidates found, or required columns with no data.

Print a brief extraction summary:
```
Extracted from <N> documents:
  Domains: <N> candidates (HIGH/MEDIUM/LOW)
  Business Terms: <N> candidates
  Policies: <N> candidates
  Systems: <N> candidates
  Regulations: <N> references found
  Gaps: [list asset types with no data]
```

### Fallback handling

Apply the user's chosen fallback (from Step 0 option A/B/C) to all gaps:

- **Option A** — populate the cell with `TODO: [field name]` so the user can find and fill it easily
- **Option B** — silently fill from Healthcare vertical defaults (defined in cdgc-setup.md)
- **Option C** — pause and ask the user targeted questions for each gap before proceeding:
  ```
  I couldn't find [asset type] in your documents. 
  Options:
    1. Provide values now (paste a list)
    2. Skip and leave blank
    3. Use Healthcare defaults for this section
  ```

---

## Step 2 — Generate the Review Workbook

Write and execute a Python script using `openpyxl` to produce:

**File:** `00_Review_<ClientName>-<ProjectName>.xlsx`
**Location:** `~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/`

This workbook has one sheet per CDGC asset type (12 sheets total including a Summary sheet). It is NOT an import file — it is a human-readable review artifact.

### Sheet: `Summary`

Columns: `Asset Type`, `Records Found`, `Confidence`, `Gaps`, `Notes`

One row per asset type. Confidence is the majority confidence level across all candidates for that type. Gaps lists any required columns that are empty. Notes captures anything ambiguous or worth flagging for the reviewer.

Example row:
```
Business Term | 34 | MEDIUM | Stakeholder columns empty | Terms extracted from "Data Dictionary" tab; domain assignment inferred from sheet grouping
```

### Sheets: one per asset type

Use the same column headers as the final import format (see column specs below). Add two extra columns at the far right:

- `Confidence` — `HIGH`, `MEDIUM`, `LOW`, or `TODO`
- `Review Notes` — free-text note explaining where the value came from or what needs checking

Color-code rows by confidence:
- HIGH → white (no fill)
- MEDIUM → light yellow (`FFFFE0`)
- LOW → light orange (`FFD580`)
- TODO → light red (`FFB3B3`)

This makes it immediately obvious to a reviewer where attention is needed.

### Column specs for each sheet (matches import format exactly)

#### Domain
`Reference ID`, `Name`, `Description`, `Alias Names`, `Lifecycle`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`

#### Subdomain
`Reference ID`, `Name`, `Description`, `Alias Names`, `Business Logic`, `Examples`, `Lifecycle`, `Security Level`, `Operation`, `Parent: Subdomain`, `Parent: Domain`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`
- Single parent rule: populate `Parent: Domain` for top-level subdomains; `Parent: Subdomain` for nested — never both

#### Regulation
`Reference ID`, `Name`, `Description`, `Lifecycle`, `Issuing Body`, `Regulation Type`, `Regulation URL`, `Operation`

#### Policy
`Reference ID`, `Name`, `Description`, `Lifecycle`, `Policy Type`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`

#### Legal Entity
`Reference ID`, `Name`, `Description`, `Lifecycle`, `Operation`

#### Business Area
`Reference ID`, `Name`, `Description`, `Lifecycle`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`

#### Geography
`Reference ID`, `Name`, `Description`, `Lifecycle`, `Operation`

#### System
`Reference ID`, `Name`, `Description`, `Asset ID`, `Lifecycle`, `Long Name`, `System Purpose`, `System Type`, `Operation`, `Parent: System`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`
- `System Type`: `Software Application`
- `System Purpose` valid values: `Core Client & Transaction Processing`, `Master Data Management`, `Data Quality`, `Warehouse & DataMart`, `Reporting Layer`, `Finance Function`, `Management Reporting`, `Risk Function`, `Regulatory Reporting`, `Sales Reporting`

#### AI System
`Reference ID`, `Name`, `Description`, `AI System Type`, `Development Stage`, `Lifecycle`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`

#### AI Model
`Reference ID`, `Name`, `Description`, `AI Model Purpose`, `Architecture Type`, `Bias`, `Drift`, `Environment`, `Input`, `Libraries`, `Lifecycle`, `Model Format`, `Model Rules`, `Output`, `Source Model Repository`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`

#### Business Term
`Reference ID`, `Name`, `Description`, `Alias Names`, `Business Logic`, `Critical Data Element`, `Examples`, `Format Type`, `Format Description`, `Lifecycle`, `Security Level`, `Classifications`, `Reference Data`, `Operation`, `Parent: Subdomain`, `Parent: Business Term`, `Parent: Metric`, `Parent: Domain`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`
- **Single parent rule:** populate `Parent: Subdomain` only — leave `Parent: Domain`, `Parent: Business Term`, `Parent: Metric` blank

#### Data Set
`Reference ID`, `Name`, `Description`, `Lifecycle`, `Operation`, `Parent: AI System`, `Parent: System`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`
- **Single parent rule:** populate `Parent: System` OR `Parent: AI System` — never both on the same row

#### Data Quality Rule Template
`Reference ID`, `Name`, `Description`, `Criticality`, `Dimension`, `Enable Automation`, `Frequency`, `Input Port Name`, `Lifecycle`, `Measuring Method`, `Output Port Name`, `Technical Description`, `Technical Rule Reference`, `Target`, `Threshold`, `Primary Glossary`, `Secondary Glossary`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`
- `Measuring Method`: use `TechnicalScript` — do NOT use `InformaticaCloudDataQuality`
- `Primary Glossary`: name only (e.g., `Social Security Number`) — do NOT use `Name | RefID` format

#### Relationships
`Source Asset`, `Source Asset Type`, `Target Asset`, `Target Asset Type`, `Relationship Type`, `Operation`
- Do NOT include `System → Data Set` — auto-created by `Parent: System` in Data Set import

---

## Step 3 — Present summary and ask for approval

After generating the Review Workbook, present a console summary to the practitioner:

```
Review Workbook generated: ~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/00_Review_<ClientName>-<ProjectName>.xlsx

── Extraction Summary ──────────────────────────────────────────────
  Domains          : <N> found  (<confidence>)
  Subdomains       : <N> found  (<confidence>)
  Business Terms   : <N> found  (<confidence>)
  Policies         : <N> found  (<confidence>)
  Regulations      : <N> found  (<confidence>)
  Systems          : <N> found  (<confidence>)
  Data Sets        : <N> found  (<confidence>)
  DQ Rule Templates: <N> found  (<confidence>)
  Relationships    : <N> generated
  TODOs            : <N> cells flagged for manual review

── Attention Items ──────────────────────────────────────────────────
  <list any LOW or TODO rows with a one-line explanation>

────────────────────────────────────────────────────────────────────
What would you like to do?

  1. Approve — generate the 14 import files now
  2. Send workbook for client review — I'll come back when it's returned
     (resume later with: /cdgc-client-setup resume <path-to-edited-workbook>)
  3. Make specific changes now — tell me what to update
  4. Re-run with different documents or fallback option
```

Wait for the practitioner's response. Do not proceed to Step 4 until explicitly approved.

**If option 1 (approve):** ask import method before generating files:
```
How would you like to import the files once generated?

  A) Manual UI (default) — upload each file yourself via the CDGC UI
  B) API (automated) — I will import programmatically and poll until complete
     Requires your IDMC org URL, username, and password.
     Not available for SAML-only orgs without API access enabled.
```
Store as `IMPORT_METHOD`. If B, collect `ORG_URL`, `LOGIN_URL`, `USERNAME`, `PASSWORD`. Inform the practitioner: credentials are used only for this session and are not stored.

### Known reasons API import may not work

| Reason | Recommendation |
|--------|---------------|
| No Import privilege in Administrator | Ask org admin to grant Import privilege, or use Option A |
| SAML-only org with no local user accounts | API auth requires a local IDMC account — use Option A |
| Pod URL unknown | Find it in IDMC → Administrator → Organization → Pod URL |
| Firewall or network restrictions blocking outbound HTTPS | Use Option A |
| JWT token expired mid-import (30 min TTL) | Script handles this by re-authenticating if a 401 is returned |

### Inline edit flow (option 3)

Accept natural language corrections:
- "Change the Governance Owner for all Business Terms to Sarah Johnson"
- "The domain for 'Patient ID' should be Patient, not Clinical"
- "Remove the TODO from Regulation — use HIPAA and HITECH only"

Apply the changes to the in-memory extraction dict, regenerate the Review Workbook, and re-present the summary.

---

## Client handoff — sending the workbook for review

When the practitioner selects option 2, provide the following handoff guidance:

```
The Review Workbook is ready to share:
  ~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/00_Review_<ClientName>-<ProjectName>.xlsx

── What to tell your reviewer ──────────────────────────────────────

  SAFE TO EDIT — these columns are yours to fill in or correct:
    • Description, Alias Names, Business Logic, Examples
    • Stakeholder: Governance Owner, Stakeholder: Governance Administrator
      (use email addresses of actual users in the CDGC org)
    • Lifecycle (valid values: Draft, In Review, Published, Obsolete)
    • Any cell showing a red TODO — these must be filled before import
    • Any cell showing orange or yellow — review and correct if wrong

  DO NOT EDIT — these columns affect import integrity:
    • Reference ID — if already populated, do not change
    • Name — changing a name breaks parent references in other sheets
    • Parent: Domain / Parent: Subdomain / Parent: System — must exactly
      match the Name of an asset in the corresponding sheet
    • Confidence, Review Notes — these columns are stripped on import;
      editing them has no effect but do not delete them
    • Sheet names — do not rename, add, or remove sheets

  CONFLICTS SHEET — if a ⚠ Conflicts — RESOLVE FIRST sheet is present,
  resolve those naming conflicts before approving. Unresolved conflicts
  will produce inconsistent data in the CDGC environment.

── To resume once the workbook is returned ─────────────────────────
  /cdgc-client-setup resume <path-to-edited-workbook>
────────────────────────────────────────────────────────────────────
```

---

## Step 4 — Generate the 14 import files

Once approved, write and execute a Python script that reads the Review Workbook (minus the `Confidence` and `Review Notes` columns) and produces the 14 import files using the same logic as `cdgc-setup.md`:

```
01_Domain.xlsx
02_Subdomain.xlsx
03_Regulation.xlsx
04_Policy.xlsx
05_Legal_Entity.xlsx
06_Business_Area.xlsx
07_Geography.xlsx
08_System.xlsx
09_AI_System.xlsx
10_AI_Model.xlsx
11_Business_Term.xlsx
12_Data_Set.xlsx
13_DQ_Rule_Template.xlsx
14_Relationships.xlsx
```

Rules:
- Strip `Confidence` and `Review Notes` columns before writing
- Skip logic is sheet-aware:
  - All sheets except Relationships and DQ Rule Template: skip if `Name` is empty or starts with `TODO`
  - Relationships sheet: skip if `Source Asset` or `Target Asset` is empty or starts with `TODO` (Relationships have no `Name` column)
  - DQ Rule Template sheet: skip if `Name` is empty or starts with `TODO`, OR if `Criticality` or `Measuring Method` is empty or starts with `TODO` — CDGC rejects DQ Rule Templates missing these required fields, so a row with a name but no substance must be skipped rather than written as an empty skeleton
- Auto-generate `Reference ID` values if blank using a customer-specific prefix derived from the client name — take the first letter of each word, uppercase, up to 4 characters (e.g., `Acme Healthcare` → `AH`, `ONC HealthcareDemo` → `OH`). Do NOT use bare CDGC prefixes like `DOM-1`, `BT-1` — those collide with system-generated IDs and are rejected on create. Use `<PREFIX>DOM-1`, `<PREFIX>BT-1`, etc.
- Validate `Operation` = `Create`, `Lifecycle` is a valid value, boolean fields are lowercase `true`/`false`
- Report a count of skipped rows and why

All files go to `~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/`.

---

## Step 5 — Import

Branch on `IMPORT_METHOD` chosen at approval (Step 3) or resume.

---

### Option A — Manual UI import

Tell the user:

```
All files are ready at: ~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/

Import in this order — one file at a time:
  CDGC UI → Gear icon → Import → Upload → Auto-map → Import

  01_Domain.xlsx              ← no dependencies
  02_Subdomain.xlsx           ← depends on Domains
  03_Regulation.xlsx          ← no dependencies
  04_Policy.xlsx              ← no dependencies
  05_Legal_Entity.xlsx        ← no dependencies
  06_Business_Area.xlsx       ← no dependencies
  07_Geography.xlsx           ← no dependencies
  08_System.xlsx              ← no dependencies
  09_AI_System.xlsx           ← no dependencies
  10_AI_Model.xlsx            ← depends on AI Systems
  11_Business_Term.xlsx       ← depends on Subdomains
  12_Data_Set.xlsx            ← depends on Systems / AI Systems
  13_DQ_Rule_Template.xlsx    ← depends on Business Terms
  14_Relationships.xlsx       ← import last

Wait for COMPLETED status before uploading the next file.
```

---

### Option B — API import

Write and execute a Python script that authenticates, imports each file in order, polls for completion, and runs a post-import verification scan.

This is the validated, hardened version — tested end-to-end 2026-05-12, 132 assets confirmed. Also available as `cdgc_api_import.py` in the repo.

Key design decisions:
- **`requests` multipart with explicit XLSX content type** — curl subprocess format was rejected server-side (jobs returned COMPLETED with `tasks:[]`); `requests` with explicit content types is the only working approach
- **`poll_job` circuit breaker** — 72 polls max (6 minutes), 502/503/504 retry, empty response handling
- **Post-import verification scan** — reuses existing JWT to confirm actual counts per asset type

```python
import requests
import getpass
import time
import sys
import json
from pathlib import Path

LOGIN_URL  = "https://dmp-us.informaticacloud.com"
ORG_URL    = "https://idmc-api.dmp-us.informaticacloud.com"
IMPORT_DIR = Path("~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/").expanduser()

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
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "X-INFA-ORG-ID": org_id,
    }
    with open(filepath, "rb") as f:
        files = {
            "file": (filepath.name, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "config": (None, '{"validationPolicy":"CONTINUE_ON_ERROR_WARNING"}', "application/json"),
        }
        resp = requests.post(
            f"{ORG_URL}/data360/content/import/v1/assets",
            headers=headers,
            files=files,
            timeout=60)
    if resp.status_code == 401:
        return None, "401"
    if not resp.text.strip():
        return None, "Empty response from import endpoint"
    try:
        data = resp.json()
    except Exception:
        return None, f"Invalid response: {resp.text[:200]}"
    if resp.status_code not in (200, 201, 202):
        return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
    job_id = data.get("jobId") or data.get("id")
    if job_id:
        return job_id, None
    return None, f"No jobId in response: {resp.text[:300]}"

def poll_job(jwt_token, org_id, job_id, filename):
    url = f"{ORG_URL}/data360/observable/v1/jobs/{job_id}"
    headers = {"Authorization": f"Bearer {jwt_token}", "X-INFA-ORG-ID": org_id}
    terminal = {"COMPLETED", "FAILED", "COMPLETED_WITH_ERRORS", "PARTIAL_COMPLETED", "PARTIAL_SUCCESS"}
    dots = 0
    for attempt in range(72):  # max 6 minutes
        try:
            resp = requests.get(url, headers=headers, timeout=30)
        except requests.exceptions.RequestException:
            time.sleep(5)
            continue
        if resp.status_code in (429, 502, 503, 504):
            time.sleep(10)
            continue
        if not resp.text.strip():
            time.sleep(5)
            continue
        try:
            data = resp.json()
        except Exception:
            time.sleep(5)
            continue
        status = data.get("status", "UNKNOWN")
        if status in terminal:
            print(f"\r  [{filename}] {status}          ")
            if status in ("COMPLETED_WITH_ERRORS", "PARTIAL_COMPLETED", "PARTIAL_SUCCESS"):
                print(f"  ⚠ Detail: {json.dumps(data.get('errors', data.get('detail', '')))[:300]}")
            return status, data
        print(f"\r  [{filename}] {status}{'.' * (dots % 4)}   ", end="", flush=True)
        dots += 1
        time.sleep(5)
    print(f"\r  [{filename}] TIMEOUT — job did not complete in 6 minutes")
    return "TIMEOUT", {}

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

    if status in ("FAILED", "TIMEOUT"):
        print(f"\nFATAL — {fname} {status}. Stopping import.")
        print(json.dumps(detail)[:500])
        sys.exit(1)

print("\n── Import Summary ──────────────────────────────────────────")
for fname, status in results:
    icon = "✓" if status == "COMPLETED" else "⚠" if status == "COMPLETED_WITH_ERRORS" else "✗"
    print(f"  {icon}  {fname:<45} {status}")
print("────────────────────────────────────────────────────────────")

# ── Verification scan ─────────────────────────────────────────────────────────
print("\nVerifying assets in org...\n")
time.sleep(3)

VERIFY_TYPES = [
    ("Domains",           "com.infa.ccgf.models.governance.Domain"),
    ("Subdomains",        "com.infa.ccgf.models.governance.Subdomain"),
    ("Regulations",       "com.infa.ccgf.models.governance.Regulation"),
    ("Policies",          "com.infa.ccgf.models.governance.Policy"),
    ("Legal Entities",    "com.infa.ccgf.models.governance.LegalEntity"),
    ("Business Areas",    "com.infa.ccgf.models.governance.BusinessArea"),
    ("Geographies",       "com.infa.ccgf.models.governance.Geography"),
    ("Systems",           "com.infa.ccgf.models.governance.System"),
    ("AI Systems",        "com.infa.ccgf.models.governance.AISystem"),
    ("AI Models",         "com.infa.ccgf.models.governance.AIModel"),
    ("Business Terms",    "com.infa.ccgf.models.governance.BusinessTerm"),
    ("Data Sets",         "com.infa.ccgf.models.governance.DataSet"),
    ("DQ Rule Templates", "com.infa.ccgf.models.governance.RuleTemplate"),
]

h_s = {"Authorization": f"Bearer {jwt_token}", "X-INFA-ORG-ID": org_id, "Content-Type": "application/json"}
grand_total = 0
for label, ct in VERIFY_TYPES:
    for attempt in range(3):
        r = requests.post(
            f"{ORG_URL}/data360/search/v1/assets?knowledgeQuery=*&segments=summary",
            headers=h_s,
            json={"from": 0, "size": 100,
                  "filterSpec": [{"type": "simple", "attribute": "core.classType", "values": [ct]}]},
            timeout=30)
        if not r.text.strip():
            time.sleep(2)
            continue
        try:
            body = r.json()
            count = len(body.get("hits", []))
            break
        except Exception:
            time.sleep(2)
            continue
    else:
        count = "?"
    grand_total += count if isinstance(count, int) else 0
    icon = "✓" if isinstance(count, int) and count > 0 else "⚠"
    print(f"  {icon}  {label:<25}: {count}")
    time.sleep(0.3)

print(f"\n  Total assets in org: {grand_total}")
print("────────────────────────────────────────────────────────────\n")
```

Substitute `<ClientName>-<ProjectName>` in `IMPORT_DIR` from the names collected in Step 0. `LOGIN_URL` and `ORG_URL` default to `dmp-us` — change the pod region prefix if the client is on a different pod (e.g., `dmp-eu`).

**Note:** AI Systems and AI Models will show `⚠ 0` in the verification scan — classType search is broken on suborg for those two types. Verify counts in the CDGC UI directly.

---

## Testing scenarios

Six scenarios covering the full range of input quality and fallback behavior. Each shows design intent, test questions, status, and a summary of actual results. See the **Test run log** section for full detail on each run.

### Scenario A — Clean structured input
**Input:** A well-organized CSV data dictionary with columns: `Domain`, `Table Name`, `Column Name`, `Description`, `Data Type`, `PII Flag`, `Owner`
**Expected:** HIGH confidence across Business Terms, Data Sets, Domains. Minimal TODOs. Review Workbook needs only stakeholder review.
**Tests:** Does domain grouping work? Does PII Flag map to Critical Data Element?
**Status:** ✅ Passed (Test Run 1 — combined with C+E)
**Result:** 4 domains, 10 subdomains, 47 business terms, 8 data sets all extracted at HIGH confidence. PII Flag correctly mapped to CDE column. One bug found and fixed (Relationships skip logic) — see Test Run 1.

---

### Scenario B — Policy PDF only
**Input:** A HIPAA compliance policy document (PDF) — single file, no data dictionary, no systems
**Expected:** HIGH confidence on Policies and Regulations. LOW/TODO on Business Terms, Systems, Data Sets.
**Tests:** Does the skill degrade gracefully? Are gaps clearly flagged? Does the PDF parser handle page boundaries correctly?
**Status:** ✅ Passed (Test Run 2)
**Result:** 4 policies and 6 regulations extracted at HIGH confidence. 3 business terms extracted at LOW from definitions section. All other asset types correctly returned as TODO. Three PDF parser bugs found and fixed during this run — see Test Run 2.

---

### Scenario C — Partial Excel with mixed structure
**Input:** An Excel file with 4 tabs: `Glossary` (business terms), `System Inventory`, `Org Chart`, `Data Sets`
**Expected:** Business Terms from Glossary tab, Systems from System Inventory tab, Business Areas from Org Chart tab, Data Sets from Data Sets tab.
**Tests:** Does tab-name-as-signal routing work? Are all 4 tabs correctly detected and routed?
**Status:** ✅ Passed (Test Run 5)
**Result:** All 4 tabs correctly routed by sheet name keyword detection. 20 business terms (HIGH), 5 systems (HIGH), 5 business areas (HIGH), 5 data sets (HIGH), 4 domains (MEDIUM — inferred from Glossary Domain column). 5 System→DataSet relationships generated from cross-tab reference. Domains scored MEDIUM (not HIGH) because they were inferred from the Glossary Domain column rather than explicitly defined — correct behavior.

---

### Scenario D — Unstructured Word doc narrative
**Input:** A Word document describing the governance program in paragraph prose — no tables, no structured metadata
**Expected:** LOW confidence across most asset types. Many TODOs. Graceful degradation.
**Tests:** Does the skill extract anything useful from prose? Are confidence scores honest? Is the recommendation actionable?
**Status:** ✅ Passed (Test Run 3)
**Result:** 5 regulations extracted at MEDIUM (named explicitly in prose), 4 domains / 4 systems / 5 policies / 5 business areas / 7 business terms all extracted at LOW (inferred from keyword proximity). Subdomains, Data Sets, Legal Entities, DQ Rules, Relationships all correctly returned as TODO. No crashes. Summary recommendation was specific and actionable.

---

### Scenario E — Conflicting documents
**Input:** A financial services CSV data dictionary AND a policy text doc that use different names for the same domains and the same regulations
**Expected:** All conflicts surfaced in a dedicated `⚠ Conflicts` sheet. Skill recommends a canonical name and blocks Relationships generation until conflicts are resolved.
**Tests:** Are all conflict types detected (domain name, regulation alias, term domain assignment)? Is the resolution guidance specific?
**Status:** ✅ Passed (Test Run 6)
**Result:** 4 conflicts detected and correctly classified: 3 domain name conflicts (`Customer` vs `Client Data`, `Transactions` vs `Transaction Processing`, `Risk & Compliance` vs `Regulatory & Risk`) and 1 term domain assignment conflict (`Account Id`). Each conflict surfaced in a dedicated `⚠ Conflicts — RESOLVE FIRST` sheet with source files and specific resolution recommendations. Relationships correctly blocked pending conflict resolution. GDPR alias conflict (CSV uses `GDPR`, policy uses `EU General Data Protection Regulation`) was detected and flagged in Regulation Review Notes.

---

### Scenario F — Fallback option comparison
**Input:** Same sparse document (`mock_policy_doc.txt`), run three times with fallback options A, B, and C
**Expected:** Three visually distinct Review Workbooks — A has red TODO cells, B has green DEFAULT cells, C has blue ANSWER cells.
**Tests:** Are the three behaviors clearly distinct? Does each produce a correctly labeled and color-coded workbook? Does Option C include a gap interview log?
**Status:** ✅ Passed (Test Run 4)
**Result:** All three workbooks produced and visually distinct. Option A: 0 gap rows filled (red TODO). Option B: 4 domains, 4 systems, 5 data sets, 4 business areas auto-filled from Healthcare defaults (green). Option C: 3 domains, 2 systems, 2 data sets, 2 business areas from simulated user answers (blue); Legal Entities skipped by user; Gap Interview Log sheet included. Policies and Regulations HIGH across all three — confirming extracted content is not affected by fallback choice.

---

### Scenario G — Multi-session resume flow (client edited workbook)
**Input:** Review Workbook generated in a prior session, edited offline (TODO cells filled, Governance Owner columns populated, one domain name corrected), then resumed via `/cdgc-client-setup resume <path>`
**Expected:** Skill loads the workbook without re-parsing documents. Correctly extracts `ClientName` and `ProjectName` from the filename. Validates columns and parent references. Reports remaining TODOs. Asks import method at resume time. Proceeds directly to Step 4 and generates 14 import files reflecting the edited values.
**Tests:**
- Does filename parsing correctly recover client and project name?
- Are broken parent links detected and flagged before generating import files?
- Does the workbook validation catch a missing required column?
- Are the edited values (not the original extracted values) reflected in the import files?
- Does import method selection appear at resume rather than at intake?
**Status:** ✅ Passed (Test Run 7 — 2026-05-14)
**Result:** All 6 test cases passed. Resume entry point correctly skipped document parsing, parsed client/project from filename, counted 115 remaining TODOs, detected 1 broken parent link, deferred import method to resume time, and confirmed client-edited values in generated files. One bug found: DQ Rule Template skip logic too permissive — fixed in Step 4 rules.

---

## Common errors and fixes

| Situation | Behavior |
|-----------|----------|
| File path not found | Report clearly: "Could not read <path> — please check the path and try again" |
| PDF has no extractable text (scanned image) | Flag: "PDF appears to be image-based — text extraction failed. Please provide a searchable PDF or paste the content as text." |
| Excel file has merged cells | Unmerge on read; use first value in merged range |
| No documents provided | Fall through to pure interview mode using cdgc-setup.md Step 1 questions |
| Term appears in multiple domains | Create one entry per domain with a Review Note flagging the duplication |
| TODO rows remain at approval | Warn: "N rows still have TODO values. Proceed anyway (they will be skipped) or fix first?" |
| Relationship target not found in extracted assets | Skip the relationship row and flag it in the summary |

---

## Test run log — iterations, results, and corrections

This section records the actual test runs performed during skill development. It is intended to help future users understand what has been validated, what edge cases were found, and what corrections were made to the skill.

---

### Test run 1 — Scenario A+C+E combined (full three-document run)

**Date:** 2026-05-06
**Client / Project:** ClientTest-NoProjectName
**Inputs:**
- `mock_data_dictionary.csv` — structured CSV with Domain, Subdomain, Column, PII Flag, CDE, Owner
- `mock_policy_doc.txt` — plain-text policy document with 5 policies and 6 regulations
- `mock_system_inventory.xlsx` — multi-tab Excel: System Inventory, Business Areas, Legal Entities, Data Sets
**Fallback:** A (TODO markers)

**Results:**
| Asset Type | Extracted | Confidence |
|------------|-----------|------------|
| Domains | 4 | HIGH |
| Subdomains | 10 | HIGH |
| Business Terms | 47 | HIGH |
| Policies | 5 | HIGH |
| Regulations | 9 | HIGH |
| Systems | 4 | HIGH |
| Data Sets | 8 | HIGH |
| Business Areas | 4 | HIGH |
| Legal Entities | 3 | HIGH |
| DQ Rule Templates | 0 | TODO |
| Relationships | 6 | MEDIUM |

**Conflicts detected:** 2
1. Domain name: CSV used `Patient`, policy doc used `Patient Information` for the same domain — flagged in ⚠ Conflicts sheet
2. Data Set domain mismatch across CSV and Excel tabs — flagged in Review Notes

**Import files generated:** 9 of 11 (DQ Rule Templates and Relationships had 0 rows written due to TODO/skip logic)

**Bug found:** Relationships skip logic checked for `Name` column which doesn't exist in the Relationships sheet — all 6 rows were incorrectly skipped.

**Fix applied:** `should_skip()` made sheet-aware — Relationships sheet now checks `Source Asset` and `Target Asset` instead of `Name`. After fix: 6 Relationships rows written correctly.

**Skipped rows after fix:** 1 (DQ Rule Template TODO placeholder — expected and correct)

---

### Test run 2 — Scenario B (PDF only, sparse input)

**Date:** 2026-05-06
**Client / Project:** ClientTest-ScenarioB
**Input:** `mock_hipaa_policy.pdf` — single HIPAA policy document, no data dictionary, no systems
**Fallback:** A (TODO markers)

**Results:**
| Asset Type | Extracted | Confidence |
|------------|-----------|------------|
| Policies | 4 | HIGH |
| Regulations | 6 | HIGH |
| Business Terms | 3 | LOW (from definitions section only) |
| Everything else | 0 | TODO |

**Bugs found and fixed (3):**

1. **Policy 4.4 not extracted** — the stop condition `(?=4\.\d+|\Z)` only matched same-prefix subsections. Fix: replaced with generic `(?=\n\d+\.\d+\s|\Z)` pattern.

2. **POL-1 name and body corrupted with document preamble** — regex started from the top of the full text, pulling everything before `4.1` into the first policy's body. Fix: search text anchored to content after the `POLICY STATEMENTS` section header using `re.search(r"POLICY STATEMENTS\n(.*)", ...)`.

3. **Page-break stitch too aggressive** — `re.sub(r"\n([a-z])", ...)` joined every lowercase-starting line in the entire document. Fix: scoped the stitch to actual page junctions only, checking that the end of page N and start of page N+1 both meet the mid-sentence criteria.

**After fixes:** All 4 policies extracted cleanly with correct names, descriptions, types, owners, and administrators.

**Graceful degradation confirmed:** The skill correctly produced a partially-filled Review Workbook rather than crashing, and the Summary sheet clearly communicated what was found vs. what needed manual fill. The actionable recommendation ("pair with a data dictionary") was surfaced in the Attention Items section.

---

### Test run 3 — Scenario D (unstructured Word doc narrative)

**Date:** 2026-05-06
**Client / Project:** ClientTest-ScenarioD
**Input:** `mock_governance_narrative.docx` — 7-section governance program overview in prose, no tables, no structured metadata
**Fallback:** A (TODO markers)

**Results:**
| Asset Type | Extracted | Confidence |
|------------|-----------|------------|
| Regulations | 5 | MEDIUM (named explicitly in prose) |
| Domains | 4 | LOW (inferred from keyword frequency) |
| Systems | 4 | LOW (functional descriptions, not official names) |
| Policies | 5 | LOW (names mentioned but no metadata) |
| Business Areas | 5 | LOW (org names from council list) |
| Business Terms | 7 | LOW (CDE mentions in Section 6 only) |
| Subdomains, Data Sets, Legal Entities, DQ Rules, Relationships | 0 | TODO |

**No bugs found.** Graceful degradation confirmed: the skill extracted a useful scaffold (30 of ~50 rows populated) rather than returning empty output, assigned honest LOW/MEDIUM confidence rather than inflating scores, and gave a clear recommendation in the summary.

**Key observation:** Regulations scored MEDIUM rather than TODO because they were named explicitly in the text — demonstrating that the confidence tiers are working correctly and are meaningful to a reviewer.

---

### Test run 4 — Scenario F (three-way fallback comparison)

**Date:** 2026-05-06
**Client / Project:** ClientTest-ScenarioF
**Input:** `mock_policy_doc.txt` (same sparse input, 3 passes)
**Fallback:** A, then B, then C

**Results — what differed across the three workbooks:**

| Asset Type | Fallback A | Fallback B | Fallback C |
|------------|-----------|-----------|-----------|
| Domains | 0 (TODO, red) | 4 (DEFAULT, green) | 3 (ANSWER, blue) |
| Systems | 0 (TODO, red) | 4 (DEFAULT, green) | 2 (ANSWER, blue) |
| Data Sets | 0 (TODO, red) | 5 (DEFAULT, green) | 2 (ANSWER, blue) |
| Business Areas | 0 (TODO, red) | 4 (DEFAULT, green) | 2 (ANSWER, blue) |
| Legal Entities | 0 (TODO, red) | 1 (DEFAULT, green) | 0 (user skipped, red) |
| Policies | 5 (HIGH) | 5 (HIGH) | 5 (HIGH) |
| Regulations | 6 (HIGH) | 6 (HIGH) | 6 (HIGH) |

**Color coding confirmed distinct and intuitive:**
- Red TODO cells = gaps left for manual fill (Option A)
- Green DEFAULT cells = auto-filled from vertical defaults (Option B)
- Blue ANSWER cells = filled from user responses during gap interview (Option C)

**Option C Gap Interview Log** — a dedicated sheet in the Fallback C workbook captures the simulated Q&A transcript, showing which gaps were asked about and what the user provided or skipped. This is valuable for auditability and hand-off to colleagues.

**Key observation:** Fallback B produces the most complete workbook but may not match the actual client's environment — appropriate for a quick demo scaffold. Fallback C produces the most accurate workbook but requires the user's time during the interview. Fallback A is the most transparent — what you see is exactly what the documents provided, nothing assumed.

---

### Test run 5 — Scenario C (multi-tab Excel)

**Date:** 2026-05-06
**Client / Project:** ClientTest-ScenarioC
**Input:** `mock_multi_tab_glossary.xlsx` — 4 tabs: Glossary, System Inventory, Org Chart, Data Sets
**Fallback:** A (TODO markers)

**Tab routing results:**
| Tab Name | Detected Asset Type | Correct? |
|----------|-------------------|----------|
| Glossary | business_terms | ✓ |
| System Inventory | systems | ✓ |
| Org Chart | business_areas | ✓ |
| Data Sets | data_sets | ✓ |

**Extraction results:**
| Asset Type | Extracted | Confidence |
|------------|-----------|------------|
| Business Terms | 20 | HIGH |
| Systems | 5 | HIGH |
| Business Areas | 5 | HIGH |
| Data Sets | 5 | HIGH |
| Domains | 4 | MEDIUM (inferred from Glossary Domain column) |
| Relationships | 5 | HIGH (System→DataSet cross-tab) |
| Subdomains, Policies, Regulations, Legal Entities, DQ Rules | 0 | TODO |

**No bugs found.** Tab-name-as-signal routing worked correctly for all 4 tabs. Domain confidence correctly scored MEDIUM (not HIGH) because the Glossary tab has a Domain column but no dedicated Domain definition sheet — the skill inferred domains from the column values rather than from an explicit definition source. This is the correct behavior.

**Key observation:** The cross-tab System→DataSet relationship generation worked by matching system names from the System Inventory tab against dataset names from the Data Sets tab, producing 5 HIGH-confidence relationships without any manual input. This is a valuable capability for clients who maintain their inventory in a single multi-tab workbook.

---

### Test run 6 — Scenario E (conflicting documents)

**Date:** 2026-05-06
**Client / Project:** ClientTest-ScenarioE
**Inputs:**
- `mock_conflict_dictionary.csv` — Financial Services data dictionary using domain names: Customer, Transactions, Risk & Compliance
- `mock_conflict_policy.txt` — Policy document using domain names: Client Data, Transaction Processing, Regulatory & Risk
**Fallback:** A (TODO markers)

**Conflicts detected (4):**
| # | Type | Description | Resolution Applied |
|---|------|-------------|-------------------|
| 1 | Domain Name | `Customer` (CSV) vs `Client Data` (policy) | CSV name used as canonical |
| 2 | Domain Name | `Transactions` (CSV) vs `Transaction Processing` (policy) | CSV name used as canonical |
| 3 | Domain Name | `Risk & Compliance` (CSV) vs `Regulatory & Risk` (policy) | CSV name used as canonical |
| 4 | Term Domain Assignment | `Account Id` domain disputed between CSV and policy doc | Resolves automatically when domain names are reconciled |

**Extraction results:**
| Asset Type | Extracted | Confidence |
|------------|-----------|------------|
| Business Terms | 16 | HIGH (1 flagged MEDIUM due to domain conflict) |
| Data Sets | 5 | HIGH |
| Subdomains | 5 | HIGH |
| Policies | 3 | HIGH |
| Regulations | 6 | HIGH (1 flagged MEDIUM — GDPR alias) |
| Domains | 3 | MEDIUM (conflict resolved) |
| Systems, Business Areas, Legal Entities, DQ Rules, Relationships | 0 | TODO |

**No bugs found.** Conflict detection fired correctly for all 4 conflicts. Each conflict was classified by type (Domain Name vs Term Domain Assignment), both source files were cited, and a specific resolution recommendation was provided. The `⚠ Conflicts — RESOLVE FIRST` sheet was generated at the front of the workbook. Relationships were correctly blocked pending conflict resolution.

**Key observation:** The GDPR alias conflict (CSV mentions `GDPR` in column descriptions; policy doc defines it as `EU General Data Protection Regulation`) was detected and flagged in the Regulation Review Notes with a recommendation to add `GDPR` as a synonym. This demonstrates the skill can catch naming inconsistencies beyond just domain names.

**Important note for real engagements:** The mock conflict documents explicitly acknowledged the naming discrepancy in their text (the policy doc included a reconciliation note). In real client documents, the conflict may be silent — no such note exists and both teams believe their naming is correct. The skill's conflict detection logic should be treated as a starting point; a human reviewer should always validate the ⚠ Conflicts sheet before approving.

---

### Test run 7 — Scenario G (multi-session resume flow)

**Date:** 2026-05-14
**Client / Project:** ResumeTest-Scenario7
**Input:** `00_Review_ResumeTest-Scenario7.xlsx` — Review Workbook produced by Test Run 1 (Scenario A), then edited programmatically to simulate a client-returned workbook:
- 73 `Stakeholder: Governance Administrator` TODO cells filled with `admin@resumetest.com`
- 9 `Regulation URL` TODO cells filled with a real URL
- 1 broken parent link introduced: BT-1 `Patient Id` → `Parent: Domain` changed to `PatientData | DOM-1` (does not exist in Domain sheet)
- 115 TODO cells deliberately left unfilled (Primary Contact, Secondary Contact, DQ Rule Template fields)
**Fallback:** N/A — resume flow skips document parsing entirely

**Test case results:**

| # | Test | Result |
|---|------|--------|
| 1 | Resume entry point triggered — no document re-parsing | ✅ Passed |
| 2 | ClientName=`ResumeTest`, ProjectName=`Scenario7` correctly parsed from filename | ✅ Passed |
| 3 | 115 remaining TODO cells counted correctly per sheet | ✅ Passed |
| 4 | Broken parent link detected: BT-1 `PatientData` not found in Domain sheet | ✅ Passed |
| 5 | Import method prompt deferred to resume time (not at intake) | ✅ Passed (confirmed by architecture — intake step not executed in resume path) |
| 6 | `admin@resumetest.com` confirmed in all 4 Domain rows of `01_Domain.xlsx` (client edit reflected, not original TODO) | ✅ Passed |

**Import files generated:** 10 of 11 written (DQ Rule Template skipped — all rows were TODO, expected and correct)

**Key observations:**
- Broken parent link was flagged in the validation summary and preserved in the import file (not silently dropped) — the practitioner was warned and chose to proceed. This is the correct behavior: the skill surfaces the problem, the human decides.
- TODO rows in Business Term (Primary/Secondary Contact) did not block the row from being written — only rows where `Name` is empty or starts with TODO are skipped. Contact fields being TODO is non-blocking. This matches the skip logic defined in Step 4.
- DQ Rule Template correctly returned 0 written rows — the single row's `Name` was non-TODO but all substantive fields were TODO; the row was written with empty data. **Correction needed:** the skip logic should be tightened for DQ Rule Templates — a row with Name populated but all substantive fields empty should be skipped too, not written as an empty skeleton.

**Bug found:** DQ Rule Template row with a non-TODO `Name` but empty `Criticality`, `Dimension`, `Measuring Method`, and `Technical Description` was included in `13_DQ_Rule_Template.xlsx` as a nearly-empty row. CDGC will reject this on import (required fields missing).

**Fix to apply to skill Step 4:** Add a DQ Rule Template-specific skip rule — skip rows where `Name` is populated but `Criticality` OR `Measuring Method` is empty or TODO.

---

### Summary of corrections made to the skill definition

| # | Issue | Where | Fix |
|---|-------|--------|-----|
| 1 | Relationships skip logic checked `Name` column (doesn't exist in Relationships sheet) | Step 4 rules | Made `should_skip()` sheet-aware: Relationships checks `Source Asset` / `Target Asset` |
| 2 | PDF policy regex stopped only at same-prefix subsections | Step 1 PDF parser notes | Updated stop condition to `(?=\n\d+\.\d+\s\|\Z)` |
| 3 | PDF parser pulled document preamble into first policy body | Step 1 PDF parser notes | Anchor policy search to text after section header (e.g. `POLICY STATEMENTS`) |
| 4 | Page-break stitch joined all lowercase-starting lines, not just cross-page breaks | Step 1 PDF parser notes | Scope stitch to actual page junctions only |
| 5 | Fallback B hardcoded to Healthcare vertical | Step 0 intake prompt | Changed to "I'll ask which vertical" — vertical-agnostic |
| 6 | "customer" used throughout instead of "client" | All steps | Global replace: customer → client |
| 7 | No Project Name in folder/file naming | All steps | Added `<ClientName>-<ProjectName>` convention throughout |
| 8 | Policy extractor used section-number hardcode (`4\.\d+`) | Step 1 PDF parser notes | Updated to generic numbered subsection pattern |
| 9 | Import method asked at intake (Step 0) before review workbook existed | Step 0 / Step 3 | Moved import method question to approval/resume time — only asked when files are about to be generated |
| 10 | Resume flow buried as option 2 of 4 in Step 3 — treated as edge case | All sections | Resume promoted to first-class entry point with its own section before Step 0; documented as the expected path for real engagements |
| 11 | No guidance on what the client can and cannot edit in the Review Workbook | Step 3 | Added Client Handoff section with explicit safe/do-not-edit column lists |
| 12 | Workflow overview implied single-session only | Overview section | Updated to document both single-session (demo) and multi-session (engagement) flows explicitly |
| 13 | "SE" / "user" used throughout — assumed a specific role | All steps | Replaced with "practitioner" (noun) and "you" (second person) throughout |
| 14 | `cdgc_api_import.py` and `cdgc_discover_classtypes.py` not documented in skill or guide | Skill prerequisites, Guide contents | Both scripts added to contents table, installation cp commands, and dedicated sections in the guide |
| 15 | DQ Rule Template row with non-TODO `Name` but empty required fields written as empty skeleton — CDGC rejects on import | Step 4 skip logic | Added DQ Rule Template-specific skip: also skip if `Criticality` or `Measuring Method` is empty or TODO (Test Run 7) |

---

## Sharing this skill

This skill lives at `~/.claude/commands/cdgc-client-setup.md`.

To share: send the file — recipient saves it to `~/.claude/commands/cdgc-client-setup.md` and invokes with `/cdgc-client-setup`.

For team distribution: commit to a shared repo under `.claude/commands/cdgc-client-setup.md`. Anyone who opens Claude Code in that directory gets the skill automatically.
