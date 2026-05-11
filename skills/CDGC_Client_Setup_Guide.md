# CDGC Client-Driven Setup — Usage Guide

## What This Package Contains

| File | Purpose |
|------|---------|
| `cdgc-client-setup.md` | The Claude Code skill — install once, use on any engagement |
| `cdgc-wipe.md` | Wipe skill — clean a CDGC org before reloading |
| `cdgc-setup.md` | Vertical demo builder — no client documents required |
| `install_cdgc_deps.sh` | Python dependency installer — run once per machine |
| `CDGC_Client_Setup_Guide.md` | This guide |

---

## What the Skill Does

`/cdgc-client-setup` builds a complete, client-specific CDGC import package from documents the client already has. Instead of generating fictional content, it reads their actual data dictionaries, policy documents, org charts, and glossaries — then maps that content to the CDGC governance model automatically.

### End-to-end flow

```
1. You provide:  client documents (PDF, Excel, CSV, Word, text)
                 client name + project name
                 fallback preference (A/B/C)

2. Claude:       parses each document
                 extracts governance assets with confidence scoring
                 detects conflicts between documents
                 generates a color-coded Review Workbook

3. You:          open the workbook, review flagged rows, approve or edit

4. Claude:       generates 14 import-ready Excel files

5. You:          import into CDGC in order, one file at a time
```

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
  pip install openpyxl pdfplumber python-docx
  ```
  Or run the included installer (see Installation below).

---

## Installation — One Time Per Machine

### Step 1 — Copy skill files to your commands folder

```bash
cp cdgc-client-setup.md ~/.claude/commands/
cp cdgc-setup.md ~/.claude/commands/
cp cdgc-wipe.md ~/.claude/commands/
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

### 1. Start the session
Type `/cdgc-client-setup` and press Enter. Claude will ask for:
- **Client name** — the organization you are working with (e.g., `Acme Health`)
- **Project name** — the engagement or workstream name (e.g., `DataGovernanceQ3`)
- **File paths** — one per line (see "What documents work well" below)
- **Fallback preference** — what to do when a field can't be inferred

### 2. Review the workbook
Claude generates `00_Review_<ClientName>-<ProjectName>.xlsx` in `~/Downloads/CDGC_Import_<ClientName>-<ProjectName>/`. Open it and review:

| Row color | Meaning | Action needed |
|-----------|---------|---------------|
| White | HIGH confidence — clear source match | None — ready to import |
| Yellow | MEDIUM confidence — inferred from context | Spot-check, confirm values |
| Orange | LOW confidence — guessed from proximity | Review carefully, correct if wrong |
| Red | TODO — could not be determined | Fill in manually before approving |
| Red (⚠ Conflicts sheet) | Naming conflict between two documents | Resolve before approving |

### 3. Approve and generate import files
When ready: tell Claude "Approve" or select option 1. Claude generates all 14 import files in the same folder.

**Alternatively:**
- **Edit offline** — make changes to the workbook, resume with `/cdgc-client-setup resume <path>`
- **Request changes inline** — tell Claude what to update in plain language ("Change the owner for all Business Terms to sarah@acme.com")

### 4. Import into CDGC
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
