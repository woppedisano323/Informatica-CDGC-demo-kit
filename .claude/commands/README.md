# Informatica CDGC Demo Kit

A ready-to-use demo environment for **Informatica Cloud Data Governance & Catalog (CDGC)**, pre-built for financial services customers. Includes all bulk import files, a Claude Code skill for generating new environments, and a Python loader script.

---

## What's included

| Path | Description |
|------|-------------|
| `sample_imports/` | 11 ready-to-import Excel files covering all CDGC asset types |
| `.claude/commands/cdgc-setup.md` | Claude Code skill — type `/cdgc-setup` to generate a new environment |
| `cdgc_glossary_loader.py` | Python REST API script for programmatic glossary loading |

---

## Sample imports — First Capital Bank (FCB)

Pre-built demo for a fictional financial services customer. Import files in this exact order:

| # | File | Asset Type | Count |
|---|------|-----------|-------|
| 01 | `01_Domain.xlsx` | Domain | 4 |
| 02 | `02_Subdomain.xlsx` | Subdomain | 9 |
| 03 | `03_Regulation.xlsx` | Regulation | 7 |
| 04 | `04_Policy.xlsx` | Policy | 5 |
| 05 | `05_Legal_Entity.xlsx` | Legal Entity | 3 |
| 06 | `06_Business_Area.xlsx` | Business Area | 8 |
| 07 | `07_System.xlsx` | System | 4 |
| 08 | `08_Business_Term_v2.xlsx` | Business Term | 31 |
| 09 | `09_Data_Set.xlsx` | Data Set | 5 |
| 10 | `10_DQ_Rule_Template_v3.xlsx` | DQ Rule Template | 10 |
| 11 | `11_Relationships_Final.xlsx` | Relationships | 25 |

**Import method:** CDGC UI → Gear icon → Import → Upload file → Import one file at a time.

> **Note:** Import Relationships last — all other assets must exist first. After importing Business Terms and Data Sets, export them to get their system Reference IDs (BT-X, DS-X) before building the Relationships file.

---

## `/cdgc-setup` Claude Code skill

Generates a complete, customized CDGC demo environment for any customer.

### Setup
1. Clone this repo
2. Open Claude Code inside the repo directory:
   ```bash
   git clone https://github.com/woppedisano323/Informatica-CDGC-demo-kit.git
   cd Informatica-CDGC-demo-kit
   claude
   ```
3. Type `/cdgc-setup` to invoke the skill

### What it does
- Asks for customer name, industry, regulatory concerns, and data domains
- Generates all 11 import files tailored to that customer
- Provides step-by-step import instructions and a confirmation checklist
- Includes pre-built defaults for 5 industry verticals:

| Vertical | Regulations | Key Focus |
|----------|------------|-----------|
| **Financial Services** | BCBS 239, CCAR, FATCA, SOX | KYC, GL, Risk |
| **Healthcare** | HIPAA, HITECH, ICD-10, FHIR | PHI, Clinical, Claims |
| **Retail & CPG** | GDPR, CCPA, PCI-DSS | Customer, Product, Supply Chain |
| **Insurance** | Solvency II, NAIC, IFRS 17, AML | Policy, Claims, Actuarial |
| **Public Sector** | FISMA, FedRAMP, Privacy Act, FOIA | Citizen, Grants, Federal Finance |

### Install globally (optional)
To use `/cdgc-setup` in any Claude Code session, not just this repo:
```bash
cp .claude/commands/cdgc-setup.md ~/.claude/commands/cdgc-setup.md
```

---

## Python loader script

`cdgc_glossary_loader.py` loads Business Terms via the IDMC REST API.

```bash
python3 cdgc_glossary_loader.py \
  --username your_username \
  --password your_password \
  --csv path/to/terms.csv \
  --dry-run
```

Remove `--dry-run` to execute the actual import.

---

## Requirements

- Python 3.x with `openpyxl` and `requests` installed:
  ```bash
  pip install openpyxl requests
  ```
- Informatica CDGC org with import permissions
- Claude Code (for the `/cdgc-setup` skill)

---

## Common import errors

| Error | Fix |
|-------|-----|
| `Enter a valid value from [Create, Update, Delete]` | Operation column missing or wrong position |
| `The parent is invalid or not present` | Import Domains before Subdomains and Business Terms |
| `Imported file contains empty values` | Remove header-only sheets from the workbook |
| Pre-validation failure | Remove Instructions/Annexure sheets |
| Relationship fails silently | Use Reference IDs (e.g., `BT-23`), not display names |
| `Parent already exists` on Relationships | Duplicate — not an error, safely ignored |
