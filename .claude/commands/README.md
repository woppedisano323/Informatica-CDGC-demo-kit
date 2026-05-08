# Claude Code Custom Skills

This directory contains custom slash command skills for Claude Code.

---

## `/cdgc-setup`

**File:** `cdgc-setup.md`  
**Purpose:** Generate a complete, importable Informatica CDGC demo environment for a customer — 14 Excel files covering every major asset type, ready to bulk-import in order.

### What it produces

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

### How to invoke

```
/cdgc-setup
```

Claude will ask for:
1. **Customer name** — used to brand descriptions and stakeholder emails
2. **Industry vertical** — see supported verticals below
3. **Key regulatory concerns** — or "use defaults" for the vertical
4. **Primary data domains** — or "use defaults"
5. **Output directory** — default: `~/Downloads/CDGC_Import_<CustomerName>/`

Providing just a customer name and vertical is enough — all other values default.

### Supported verticals

#### Financial Services
Banks, credit unions, capital markets, insurance carriers, and fintech.

| Asset Type | Count |
|-----------|-------|
| Domains | 4–5 |
| Subdomains | 9–12 |
| Regulations | 7–9 (BCBS 239, CCAR, FATCA, BSA/AML, SOX, MiFID II, GDPR) |
| Policies | 5–8 |
| Legal Entities | 4–6 |
| Business Areas | 6–12 |
| Geographies | 6–10 |
| Systems | 4–8 (Systems + AI Systems) |
| AI Models | 4–9 |
| Business Terms | 30–40 |
| Data Sets | 5–10 |
| DQ Rule Templates | 10–15 |
| Relationships | 25–50 |

#### Healthcare
Hospitals, health systems, payers, and life sciences.

| Asset Type | Count |
|-----------|-------|
| Domains | 4 (Patient, Clinical, Claims & Billing, Compliance & Privacy) |
| Subdomains | 9 |
| Regulations | 6 (HIPAA, HITECH, CMS CoP, FDA 21 CFR Part 11, HL7 FHIR, ICD-10) |
| Policies | 5 |
| Systems | 4 (EHR, Claims Management, Clinical Data Warehouse, Regulatory Reporting) |
| Business Terms | 28 |
| Data Sets | 5 |
| DQ Rule Templates | 10 |
| Relationships | 25 |

#### Retail & CPG
Retailers, consumer goods, e-commerce, and grocery.

| Asset Type | Count |
|-----------|-------|
| Domains | 4 (Customer, Product, Supply Chain, Transactions) |
| Subdomains | 9 |
| Regulations | 5 (GDPR, CCPA, PCI-DSS, California Prop 65, GS1 Standards) |
| Policies | 5 |
| Systems | 4 (POS, E-Commerce Platform, ERP/Inventory, Customer Data Platform) |
| Business Terms | 28 |
| Data Sets | 5 |
| DQ Rule Templates | 10 |
| Relationships | 25 |

#### Insurance
Property & casualty, life, health carriers, reinsurance, and brokerage.

| Asset Type | Count |
|-----------|-------|
| Domains | 4 (Policy & Underwriting, Claims, Customer, Risk & Compliance) |
| Subdomains | 9 |
| Regulations | 7 (Solvency II, NAIC Model Laws, IFRS 17, State DOI, GDPR, CCPA, AML) |
| Policies | 5 |
| Systems | 4 (Policy Admin, Claims Management, Actuarial Modeling, Regulatory Reporting) |
| Business Terms | 28 |
| Data Sets | 5 |
| DQ Rule Templates | 10 |
| Relationships | 25 |

#### Public Sector & Government
Federal, state, and local agencies, defense, and public utilities.

| Asset Type | Count |
|-----------|-------|
| Domains | 4 (Citizen Services, Program & Operations, Financial Management, Compliance & Reporting) |
| Subdomains | 9 |
| Regulations | 7 (FISMA, FedRAMP, OMB A-123, NIST 800-53, Privacy Act, FOIA, ATO) |
| Policies | 5 |
| Systems | 4 (Case Management, Financial Management, Grants Management, Data Analytics Platform) |
| Business Terms | 28 |
| Data Sets | 5 |
| DQ Rule Templates | 10 |
| Relationships | 25 |

---

### Import order

Always import in file number order — CDGC validates parent references at import time.

```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14
```

Wait for COMPLETED status in the CDGC UI before uploading the next file. Import `14_Relationships.xlsx` last — all referenced assets must exist first.

**Import method:** CDGC UI → Gear icon → Import → Upload file → Map columns → Import (one file at a time).

---

### Sharing this skill

**With a colleague:** Send them `cdgc-setup.md`. They save it to `~/.claude/commands/cdgc-setup.md` and type `/cdgc-setup` in any Claude Code session.

**With a team via git:** Add `cdgc-setup.md` to a shared repo under `.claude/commands/cdgc-setup.md` at the repo root. Anyone who clones the repo and opens Claude Code in that directory gets the skill automatically.

**Via plugin marketplace (advanced):** Package with a `plugin.json` manifest and distribute via a private marketplace URL. Team members install with `claude plugin add <marketplace-url>`.
