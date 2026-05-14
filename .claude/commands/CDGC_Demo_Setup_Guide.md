# CDGC Demo Environment Setup — Usage Guide

## What This Skill Does

`/cdgc-setup` generates a complete, importable CDGC demo environment tailored to a client's industry vertical. Instead of using real client documents, it produces realistic content — domains, business terms, policies, regulations, systems, DQ rules, and relationships — that matches the client's industry context. The result is a demo that looks real, passes governance scorecard checks, and can be stood up in under an hour.

**When to use `/cdgc-setup` vs `/cdgc-client-setup`:**

| Situation | Use |
|-----------|-----|
| No client documents available, or running a quick vertical demo | `/cdgc-setup` — generates realistic content from vertical defaults |
| Client has data dictionaries, policy PDFs, glossaries, or org charts | `/cdgc-client-setup` — uses the client's actual content |
| Mid-engagement: client provided docs after the initial demo | `/cdgc-client-setup` — replace demo content with client-specific assets |

---

## Workflow

```
1. /cdgc-setup
2. Provide: client name, industry vertical, regulatory concerns, primary domains
   (client name + vertical is enough — all other values default)
3. Choose import method: A) Manual UI  or  B) API automated
   (if B, provide your IDMC org URL, username, and password)
4. Claude generates 14 import-ready Excel files
5. Import into CDGC in order, one file at a time
```

---

## What It Produces

14 Excel files covering every major CDGC asset type:

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

Output goes to: `~/Downloads/CDGC_Import_<ClientName>/`

---

## Supported Verticals

### Financial Services
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

### Healthcare
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

### Retail & CPG
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

### Insurance
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

### Public Sector & Government
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

### Oil & Gas
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

### Manufacturing
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

## Importing into CDGC

### Option A — Manual UI

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

### Option B — API (automated)

If you chose API import at the start, Claude generates and runs the import script automatically — no manual steps required. It authenticates, uploads each file, polls for COMPLETED status, and prints a verification scan when done.

To run the standalone script independently:
```bash
pip install requests
python3 ~/.claude/commands/cdgc_api_import.py
```

Edit `IMPORT_DIR` at the top of the script to match your client folder. Change `LOGIN_URL` / `ORG_URL` if your org is on a pod other than `dmp-us`.

| Known issue | Resolution |
|------------|-----------|
| No Import privilege | Ask org admin to grant it, or use Option A |
| SAML-only org | API auth requires a local IDMC account — use Option A |
| Pod URL unknown | IDMC → Administrator → Organization → Pod URL |
| AI Systems / AI Models show ⚠ 0 in verification scan | classType search is broken on suborg for those two types — verify counts in the CDGC UI directly |

---

## CDGC and Data Marketplace setup order

> **Set up CDGC before Data Marketplace.** CDGC provides the governance foundation — domains, business terms, policies, and DQ rules — that Data Marketplace surfaces to data consumers. Without CDGC in place, Marketplace collections will lack linked glossary terms, certified definitions, and DQ scores.

**Recommended order:**
1. Import CDGC assets using `/cdgc-setup`
2. Import Data Marketplace assets using `/marketplace-setup`
3. In CDGC, link Data Sets to Data Collections via the Relationships import
4. In Marketplace, verify that Data Collections surface linked CDGC Business Terms

---

## Resetting a Demo Environment

Before re-running or switching verticals, wipe the org first:

```
/cdgc-wipe
```

This deletes all governance assets in dependency order (children before parents). Always confirm the org URL before proceeding — the wipe is irreversible. Intended for sandbox and demo orgs only.

---

## Questions or Feedback

Raise issues or suggestions in the `Informatica-CDGC-kit` repository.
