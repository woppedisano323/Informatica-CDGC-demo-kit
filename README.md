**Informatica CDGC Custom Demo Generator:**

**File:** `cdgc-setup.md`  

**Purpose:** Generate a complete, importable Informatica CDGC demo environment tailored to a specific customer and industry vertical. The skill produces 14 Excel files that together cover every major CDGC asset type — Domains, Subdomains, Regulations, Policies, Legal Entities, Business Areas, Geographies, Systems, AI Systems, AI Models, Business Terms, Data Sets, DQ Rule Templates, and cross-asset Relationships. All content (names, descriptions, stakeholder emails, regulatory references, and data quality rules) is generated to match the customer's industry context. Files are formatted for CDGC's bulk import mechanism and sequenced so that parent assets always exist before their children are imported. The result is a demo environment that looks real, passes governance scorecard checks, and can be stood up in under an hour.

---

### Important: CDGC and Data Marketplace setup order

> **Set up CDGC before Data Marketplace** to get full value from both tools. CDGC provides the governance foundation — domains, business terms, policies, and data quality rules — that Data Marketplace surfaces to data consumers. Without CDGC in place, Data Marketplace collections will lack linked glossary terms, certified definitions, and DQ scores.

**Recommended order:**
1. Import CDGC assets using `/cdgc-setup` (this skill)
2. Import Data Marketplace assets using `/marketplace-setup`
3. In CDGC, link Data Sets to Data Collections via the Relationships import
4. In Marketplace, verify that Data Collections surface linked CDGC Business Terms

---

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
| Systems | 4–6 |
| AI Systems | 2–4 |
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
| Legal Entities | 3–4 |
| Business Areas | 5–6 |
| Geographies | 5–8 |
| Systems | 4 (EHR, Claims Management, Clinical Data Warehouse, Regulatory Reporting) |
| AI Systems | 2–3 |
| AI Models | 4–5 |
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
| Legal Entities | 3–4 |
| Business Areas | 5–6 |
| Geographies | 5–8 |
| Systems | 4 (POS, E-Commerce Platform, ERP/Inventory, Customer Data Platform) |
| AI Systems | 2–3 |
| AI Models | 4–5 |
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
| Legal Entities | 3–4 |
| Business Areas | 5–6 |
| Geographies | 5–8 |
| Systems | 4 (Policy Admin, Claims Management, Actuarial Modeling, Regulatory Reporting) |
| AI Systems | 2–3 |
| AI Models | 4–5 |
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
| Legal Entities | 3–4 |
| Business Areas | 5–6 |
| Geographies | 5–8 |
| Systems | 4 (Case Management, Financial Management, Grants Management, Data Analytics Platform) |
| AI Systems | 2–3 |
| AI Models | 4–5 |
| Business Terms | 28 |
| Data Sets | 5 |
| DQ Rule Templates | 10 |
| Relationships | 25 |

#### Oil & Gas
Upstream E&P, midstream pipeline, downstream refining, oilfield services, and integrated energy companies.

| Asset Type | Count |
|-----------|-------|
| Domains | 4 (Assets & Operations, HSE & Compliance, Supply Chain & Procurement, Finance & Commercial) |
| Subdomains | 9 |
| Regulations | 7 (BSEE, EPA Clean Air Act, EPA Clean Water Act, PHMSA, OSHA PSM, SEC Reg S-X, EITI) |
| Policies | 5 |
| Legal Entities | 3–4 |
| Business Areas | 5–6 |
| Geographies | 5–8 |
| Systems | 4 (SCADA/Historian, Enterprise Asset Management, Production Accounting, HSE Management) |
| AI Systems | 2–3 |
| AI Models | 4–5 |
| Business Terms | 28 |
| Data Sets | 5 |
| DQ Rule Templates | 10 |
| Relationships | 25 |

#### Manufacturing
Discrete and process manufacturing, industrial equipment, automotive, aerospace & defense, and consumer goods production.

| Asset Type | Count |
|-----------|-------|
| Domains | 4 (Product & Engineering, Production & Operations, Quality, Supply Chain) |
| Subdomains | 9 |
| Regulations | 6 (ISO 9001, ISO 14001, OSHA, EPA TRI, ITAR, RoHS/REACH) |
| Policies | 5 |
| Legal Entities | 3–4 |
| Business Areas | 5–6 |
| Geographies | 5–8 |
| Systems | 4 (ERP/MES, Product Lifecycle Management, Quality Management, Supply Chain Planning) |
| AI Systems | 2–3 |
| AI Models | 4–5 |
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

---

## Skills included in this repo

All three skills are in `.claude/commands/` and are **auto-loaded** when you open this repo in Claude Code — no manual install required.

| Skill | Purpose |
|-------|---------|
| `/cdgc-setup` | Generate a full CDGC demo environment for any vertical — no client documents required |
| `/cdgc-client-setup` | Build a CDGC environment from the client's actual documents (data dictionaries, policy PDFs, org charts) |
| `/cdgc-wipe` | Wipe all governance assets from a CDGC org before reloading |

### Getting started

```bash
# Clone the repo and open in Claude Code
git clone https://github.com/woppedisano323/Informatica-CDGC-demo-kit.git
cd Informatica-CDGC-demo-kit

# Install Python dependencies (required for /cdgc-client-setup)
pip install openpyxl pdfplumber python-docx
```

Then type `/cdgc-setup`, `/cdgc-client-setup`, or `/cdgc-wipe` in Claude Code.

### Usage guide

See `.claude/commands/CDGC_Client_Setup_Guide.md` for the full guide — demo script, document tips, troubleshooting, and validated demo document set.
