# Claude Code Custom Skills — CDGC Demo Kit

This directory contains the Claude Code slash command skills for Informatica CDGC demos. Skills are auto-loaded when you open this repo in Claude Code — no manual install required.

---

## Skills at a glance

| Skill | File | Purpose |
|-------|------|---------|
| `/cdgc-setup` | `cdgc-setup.md` | Generate a full CDGC demo environment for any vertical — no client documents required |
| `/cdgc-client-setup` | `cdgc-client-setup.md` | Build a CDGC environment from the client's actual documents |
| `/cdgc-wipe` | `cdgc-wipe.md` | Wipe all governance assets from a CDGC org before reloading |

**Not sure which to use?**
- Client has data dictionaries, policy PDFs, or glossaries → `/cdgc-client-setup`
- No client documents, or running a quick vertical demo → `/cdgc-setup`
- Need to clear a demo org before reloading → `/cdgc-wipe`

---

## `/cdgc-setup`

Generate a complete, importable CDGC demo environment for any industry vertical. Produces 14 Excel files covering every major asset type, ready to bulk-import in order.

**Invoke:** `/cdgc-setup`

Claude will ask for: customer name, industry vertical, regulatory concerns, primary domains, and output directory. Customer name + vertical is enough — all other values default.

**Supported verticals:** Financial Services, Healthcare, Retail & CPG, Insurance, Public Sector & Government, Oil & Gas, Manufacturing

**What it produces:**

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

**Import order:** `01 → 02 → 03 → ... → 14` — always in sequence, one file at a time, wait for COMPLETED before uploading the next.

---

## `/cdgc-client-setup`

Build a complete CDGC import package from documents the client already has — data dictionaries, policy PDFs, org charts, glossaries, Excel schemas. Parses the documents, scores confidence, generates a color-coded Review Workbook for approval, then produces all 14 import files.

**Invoke:** `/cdgc-client-setup`

Claude will ask for: client name, project name, file paths to their documents, and fallback preference (A/B/C).

**Accepts:** CSV, Excel (multi-tab), PDF, Word, plain text

**Fallback options when a field can't be inferred:**
- **A** — TODO markers for manual review
- **B** — auto-fill from vertical defaults
- **C** — interactive gap interview

**Review Workbook color guide:**

| Color | Meaning |
|-------|---------|
| White | HIGH confidence — ready to import |
| Yellow | MEDIUM — spot-check recommended |
| Orange | LOW — review carefully |
| Red | TODO or conflict — action required |

**Prerequisites:** Python 3.8+ and `pip install openpyxl pdfplumber python-docx` (or run `install_cdgc_deps.sh`)

**Full usage guide:** See `CDGC_Client_Setup_Guide.md` in this directory.

**Validated demo document set (Healthcare):**
Three authentic HHS/ONC/CMS PDFs in `~/Downloads/CDGC_Demo_Docs/` — use with client name `ONC`, project `HealthcareDemo`.

---

## `/cdgc-wipe`

Wipe all governance assets from a CDGC org. Authenticates via IDMC JWT, scans all asset types, confirms total count, then deletes in dependency order (children before parents). Loops until 404 confirms each asset is fully gone.

**Invoke:** `/cdgc-wipe`

**Requires:** IDMC username and password (entered at runtime, never stored)

**Deletes in order:** DQ Rule Templates → Business Terms → Data Sets → AI Models → AI Systems → Systems → Business Areas → Legal Entities → Geographies → Policies → Regulations → Subdomains → Domains

**Warning:** Destructive and irreversible. Intended for sandbox and demo orgs only. Always confirms count and requires you to type `CONFIRM` before deleting anything.

---

## Import method (all skills)

**CDGC UI → Gear icon → Import → Upload → Auto-map → Import**

One file at a time. Wait for **COMPLETED** status before uploading the next file.
