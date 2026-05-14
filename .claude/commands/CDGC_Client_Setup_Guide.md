# CDGC Client-Driven Setup — Usage Guide

## What This Package Contains

| File | Purpose |
|------|---------|
| `cdgc-client-setup.md` | The Claude Code skill — install once, use on any engagement |
| `cdgc-wipe.md` | Wipe skill — clean a CDGC org before reloading |
| `cdgc-setup.md` | Vertical demo builder — no client documents required |
| `cdgc_api_import.py` | Standalone API import script — authenticate, import 14 files in order, poll for completion, verify counts. Validated end-to-end 2026-05-12. |
| `cdgc_discover_classtypes.py` | Diagnostic utility — query the CDGC API to list asset counts and externalIds by type. Use before/after import to verify org state. |
| `install_cdgc_deps.sh` | Python dependency installer — run once per machine |
| `CDGC_Client_Setup_Guide.md` | This guide — `/cdgc-client-setup` workflow, resume flow, document tips, troubleshooting |
| `CDGC_Demo_Setup_Guide.md` | Companion guide — `/cdgc-setup` verticals, asset counts, import instructions |

---

## What the Skill Does

`/cdgc-client-setup` builds a complete, client-specific CDGC import package from documents the client already has. Instead of generating fictional content, it reads their actual data dictionaries, policy documents, org charts, and glossaries — then maps that content to the CDGC governance model automatically.

---

## Workflow

**Which path are you on?**

- **Have source documents and want to run now?** → Path A below
- **Have a Review Workbook already generated (or returned by the client)?** → `/cdgc-client-setup resume <path>`

---

### Path A — Single-session (demo or proof of concept)

Everything happens in one sitting. The practitioner stays in Claude Code throughout.

```
1. /cdgc-client-setup
2. Provide: client name, project name, source documents, fallback preference (A/B/C)
3. Claude parses documents → generates Review Workbook
   Output: ~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/00_Review_<ClientName>-<ProjectName>.xlsx
4. Review inline (white = ready, yellow = spot-check, orange = review, red = action required)
5. Approve → choose import method (UI or API)
6. Claude generates 14 import files in the same folder
7. Import into CDGC in order (01 → 14), one file at a time, wait for COMPLETED each
```

---

### Path B — Multi-session (real client engagement)

The review cycle happens outside Claude Code. The workbook is the handoff artifact.

```
Session 1 — practitioner has source documents:
  1. /cdgc-client-setup
  2. Provide: client name, project name, source documents, fallback preference (A/B/C)
  3. Claude parses documents → generates Review Workbook
     Output: ~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/00_Review_<ClientName>-<ProjectName>.xlsx
  4. Choose "Send for client review" → Claude provides handoff instructions
  5. Share workbook with client team

  [Client fills in owners, corrects terms, resolves conflicts — days or weeks]

Session 2 — workbook returned (any practitioner, any machine):
  6. /cdgc-client-setup resume ~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/00_Review_<ClientName>-<ProjectName>.xlsx
  7. Claude validates workbook → reports remaining TODOs + broken parent links
  8. Choose import method (UI or API)
  9. Claude generates 14 import files
  10. Import into CDGC in order (01 → 14), one file at a time, wait for COMPLETED each
```

> For the `/cdgc-setup` (vertical demo) workflow, see `CDGC_Demo_Setup_Guide.md`.

### Output files

| # | File | Asset Type |
|---|------|-----------|
| 01 | `01_Domain.xlsx` | Domain |
| 02 | `02_Subdomain.xlsx` | Subdomain |
| 03 | `03_Regulation.xlsx` | Regulation |
| 04 | `04_Policy.xlsx` | Policy |
| 05 | `05_Legal_Entity.xlsx` | Legal Entity |
| 06 | `06_Business_Area.xlsx` | Business Area |
| 07 | `07_Geography.xlsx` | Geography |
| 08 | `08_System.xlsx` | System |
| 09 | `09_AI_System.xlsx` | AI System |
| 10 | `10_AI_Model.xlsx` | AI Model |
| 11 | `11_Business_Term.xlsx` | Business Term |
| 12 | `12_Data_Set.xlsx` | Data Set |
| 13 | `13_DQ_Rule_Template.xlsx` | DQ Rule Template |
| 14 | `14_Relationships.xlsx` | Cross-asset relationships |

---

## When to Use This vs `/cdgc-setup`

| Situation | Use |
|-----------|-----|
| Client has data dictionaries, policy PDFs, glossaries, or org charts | `/cdgc-client-setup` |
| No client documents, or running a quick vertical demo | `/cdgc-setup` |
| Mid-engagement: client provided docs after initial demo | `/cdgc-client-setup` |
| Demonstrating the AI-assisted onboarding story to a prospect | `/cdgc-client-setup` |

**Key distinction:** `/cdgc-setup` generates content that *looks* real. `/cdgc-client-setup` uses content that *is* real — the client's own vocabulary, policies, and domain structure.

---

## Prerequisites

- **Claude Code** installed and running on your machine
- **Python 3.8 or later** (`python3 --version` to check)
- Required Python packages:
  ```bash
  pip install openpyxl pdfplumber python-docx requests
  ```
  (`requests` is required for API import — Option B at approval time)

  Or run the included installer (see Installation below).

---

## Installation — One Time Per Machine

### Step 1 — Copy skill files to your commands folder

```bash
cp cdgc-client-setup.md ~/.claude/commands/
cp cdgc-setup.md ~/.claude/commands/
cp cdgc-wipe.md ~/.claude/commands/
cp cdgc_api_import.py ~/.claude/commands/
cp cdgc_discover_classtypes.py ~/.claude/commands/
cp install_cdgc_deps.sh ~/.claude/commands/
cp CDGC_Client_Setup_Guide.md ~/.claude/commands/
```

> **Windows:** The commands folder is at `%USERPROFILE%\.claude\commands\`

### Step 2 — Run the dependency installer

```bash
~/.claude/commands/install_cdgc_deps.sh
```

You will see a confirmation message when complete. If you get a permissions error:
```bash
chmod +x ~/.claude/commands/install_cdgc_deps.sh && ~/.claude/commands/install_cdgc_deps.sh
```

### Step 3 — Verify the skills are available

Open Claude Code and type `/cdgc` — you should see:
- `/cdgc-setup` — vertical demo builder
- `/cdgc-client-setup` — document ingestion
- `/cdgc-wipe` — org wipe

---

## Using the Skill — Step by Step

### Starting from source documents

Type `/cdgc-client-setup` and press Enter. Claude will ask for:
- **Client name** — the organization you are working with (e.g., `Acme Health`)
- **Project name** — the engagement or workstream name (e.g., `DataGovernanceQ3`)
- **File paths** — one per line (see "What documents work well" below)
- **Fallback preference** — what to do when a field can't be inferred

Import method is **not** asked at this point — it's asked later, only when you are ready to generate import files.

### Starting from an edited workbook (resume flow)

If the Review Workbook was generated in a previous session or returned by the client after review, skip document parsing and load directly:

```
/cdgc-client-setup resume ~/Downloads/CDGC_Import_AcmeHealth-DataGovernanceQ3/00_Review_AcmeHealth-DataGovernanceQ3.xlsx
```

Claude will:
1. Parse the client and project name from the filename
2. Validate all sheets, columns, and parent references
3. Report remaining TODOs and any broken parent links
4. Ask which import method you want (A or B), then generate the 14 files

This is the expected entry point for real engagements where the review cycle happened outside of Claude Code.

### Reviewing the workbook

Claude generates `00_Review_<ClientName>-<ProjectName>.xlsx` in `~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/`. Open it and review:

| Row color | Meaning | Action needed |
|-----------|---------|---------------|
| White | HIGH confidence — clear source match | None — ready to import |
| Yellow | MEDIUM confidence — inferred from context | Spot-check, confirm values |
| Orange | LOW confidence — guessed from proximity | Review carefully, correct if wrong |
| Red | TODO — could not be determined | Fill in manually before approving |
| Red (⚠ Conflicts sheet) | Naming conflict between two documents | Resolve before approving |

### What the reviewer can and cannot edit

**Safe to edit:**
- Description, Alias Names, Business Logic, Examples
- Stakeholder: Governance Owner, Stakeholder: Governance Administrator *(use email addresses of actual CDGC org users)*
- Lifecycle *(valid values: Draft, In Review, Published, Obsolete)*
- Any red TODO cell — these must be filled before import
- Any yellow or orange cell — correct if the extracted value is wrong

**Do not edit:**
- Reference ID — if already populated, do not change
- Name — changing a name breaks parent references in other sheets
- Parent: Domain / Parent: Subdomain / Parent: System — must exactly match the Name of an asset in the corresponding sheet
- Confidence, Review Notes columns — stripped on import; editing has no effect but do not delete them
- Sheet names — do not rename, add, or remove sheets

### Approving and generating import files

Tell Claude "Approve" or select option 1. Claude will then ask for import method (A or B) and generate all 14 files.

**Alternatively:**
- **Send for client review** — select option 2; Claude provides handoff guidance including the safe/do-not-edit instructions to pass along
- **Request inline changes** — tell Claude what to update in plain language ("Change the owner for all Business Terms to sarah@acme.com")

### Importing into CDGC

#### Option A — Manual UI

**CDGC UI → Gear icon → Import → Upload → Auto-map → Import**

Import in order, one file at a time. Wait for **COMPLETED** status before uploading the next file.

```
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
```

#### Option B — API (automated)

If you selected API import in Step 1, Claude generates and runs the import script automatically — no manual steps required. It authenticates, uploads each file, polls for COMPLETED status, and prints a verification scan when done.

To run the standalone script outside of the skill:
```bash
pip install requests
python3 ~/.claude/commands/cdgc_api_import.py
```

Edit `IMPORT_DIR` at the top of the script to match your engagement folder (e.g., `CDGC_Import_AcmeHealth-DataGovernanceQ3`). Change `LOGIN_URL` / `ORG_URL` if your org is on a pod other than `dmp-us`.

| Known issue | Resolution |
|------------|-----------|
| No Import privilege | Ask org admin to grant it, or use Option A |
| SAML-only org | API auth requires a local IDMC account — use Option A |
| Pod URL unknown | IDMC → Administrator → Organization → Pod URL |
| AI Systems / AI Models show ⚠ 0 in verification scan | classType search is broken on suborg for those two types — verify counts in the CDGC UI directly |

---

## Diagnostic Utility — `cdgc_discover_classtypes.py`

Use this script to inspect what's in a CDGC org before or after import — useful for validating a clean slate before a demo reload or confirming asset counts after import.

```bash
python3 ~/.claude/commands/cdgc_discover_classtypes.py
```

It prompts for credentials, then prints a table of asset counts and externalIds for all 13 governance asset types.

---

## What Documents Work Well

### Best inputs (HIGH confidence extraction)
| Document type | What gets extracted |
|---------------|-------------------|
| Data dictionary (CSV or Excel with Term/Description/Domain columns) | Business Terms, Domains, Subdomains, Data Sets |
| Multi-tab Excel (Glossary / Systems / Org Chart / Data Sets tabs) | All asset types, often HIGH across the board |
| HIPAA or compliance policy PDF | Policies, Regulations |
| Numbered section policy document | Policies (section numbers become policy structure) |

### Good inputs (MEDIUM confidence)
| Document type | What gets extracted |
|---------------|-------------------|
| Architecture or system inventory doc | Systems, Data Sets |
| Org chart or department list | Business Areas |
| Governance program narrative (Word) | Regulations (named explicitly), Domains, Business Areas at LOW |

### Poor inputs (LOW confidence or empty)
| Document type | Why |
|---------------|-----|
| Scanned PDF (image-based) | No extractable text — skill flags and skips |
| Slide deck (PowerPoint) | Not supported — convert to PDF first |
| Dense legal contract | Policy signals present but buried — usually LOW |

### Tips for better extraction
- Provide documents from the same organization — cross-org documents introduce vocabulary conflicts the skill can't resolve
- More documents = better coverage; 2–4 well-chosen documents outperforms 1 comprehensive one
- For PDFs, searchable (not scanned) versions extract cleanly
- Column header names matter — "Domain", "Owner", "Description" extract at HIGH; "Dept", "Resp Party", "Def" may extract at MEDIUM

---

## Validated Demo Document Set — Healthcare / HHS

For demos, use these three authentic publicly available PDFs. They come from the same HHS/CMS/ONC ecosystem, produce natural vocabulary conflicts, and demonstrate the full skill capability with under 50 business terms (demo-friendly).

| File | Source | What it contributes |
|------|--------|-------------------|
| `USCDI_V6_July2025.pdf` | ONC (HealthIT.gov) | 21 data classes → Domains, Subdomains, Business Terms (HIGH) |
| `HHS_OCR_privacysummary.pdf` | HHS Office for Civil Rights | HIPAA policy sections → Policies, Regulations (HIGH) |
| `EnterpriseDataPlanning.pdf` | CMS | Subject Areas, Data Stewards → Domains, Systems, Data Sets (MEDIUM) |

**Keep source documents at:** `~/Downloads/CDGC_Demo_Docs/`
**Output goes to:** `~/Downloads/CDGC_Import_ONC-HealthcareDemo/`
**Invoke with:** Client name `ONC`, Project name `HealthcareDemo`

**Why these three documents work well as a demo:**
- Same organizational family (HHS/ONC/CMS) — coherent governance context
- Three different vocabularies for overlapping concepts — generates 2 natural conflicts the skill correctly flags
- Realistic asset counts — 4 domains, 30 business terms, 5 policies, 6 regulations — large enough to be credible, small enough to review live

---

## Demo Script — What to Say

**Opening:** "One of the most time-consuming parts of a CDGC rollout is loading your governance content. Most clients already have it somewhere — a data dictionary, a compliance policy, maybe an org chart. This skill reads those documents and maps them to CDGC automatically."

**During parsing:** "Claude is reading each document and identifying governance assets — terms, policies, domains, systems. It assigns a confidence score to each one based on how clearly it was defined in the source."

**Showing the Review Workbook:** "This is the Review Workbook. White rows are ready to import — the skill is confident it got them right. Yellow and orange rows are where it had to infer — these are the spots your team would review before we go live. The red rows are gaps — either the document didn't have that information, or it's something we'd fill in together."

**Showing the Conflicts sheet:** "This is something most governance tools miss. When two documents use different names for the same thing — for example, one team calls it 'Patient Demographics' and another calls it 'PHI' — the skill flags it here rather than silently picking one. These conflicts are real ones your governance team would need to resolve anyway. We're just surfacing them earlier."

**Approval and import:** "Once you approve, it generates 14 import files in the exact format CDGC expects. You upload them in order — one file at a time — and your governance environment is live."

---

## Conflict Detection

When two documents use different names for the same domain or term, the skill flags it in a dedicated **⚠ Conflicts — RESOLVE FIRST** sheet. Each entry includes:
- Conflict type (Domain Name, Term Domain Assignment, Regulation Alias)
- Which source document uses which name
- A recommended resolution

Resolve all conflicts before approving. If you approve with unresolved conflicts, one version is used without acknowledgment — which creates inconsistency in the imported environment.

---

## Fallback Options

| Option | What happens when a field can't be inferred | Best for |
|--------|---------------------------------------------|----------|
| A — TODO markers | Red TODO cells — find and fill manually | Most transparent; real engagements |
| B — Vertical defaults | Auto-filled from Healthcare/FinServ/etc defaults | Quick demos; proof of concept |
| C — Gap interview | Claude asks you for each missing value before generating | Thorough onboarding; client present |

---

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| `/cdgc-client-setup` doesn't appear | Confirm `cdgc-client-setup.md` is in `~/.claude/commands/` |
| `ModuleNotFoundError` during execution | Re-run `install_cdgc_deps.sh` |
| PDF extracts no text | PDF is image-based (scanned). Request a searchable PDF or paste content as text |
| Excel with merged cells | Handled automatically — merged values are inherited downward |
| TODO rows remain at approval | You will be warned; choose to proceed (TODO rows are skipped in import files) or fix first |
| Conflict sheet appears | Resolve naming conflicts in the ⚠ Conflicts sheet before approving |
| Import fails with "multiple parents" | Review Data Set and Business Term rows — each must have exactly one parent column populated |
| Import fails with "invalid Primary Glossary" | DQ Rule Template Primary Glossary must use term name only, not `Name \| RefID` format |

---

## Resetting a Demo Environment

Before re-running a demo or testing a different document set, wipe the CDGC org first:

```
/cdgc-wipe
```

This deletes all governance assets in the correct dependency order (children before parents). Always confirm the org URL before proceeding — the wipe is irreversible.

---

## Questions or Feedback

Raise issues or suggestions in the `cdgc-demo-kit` repository.
