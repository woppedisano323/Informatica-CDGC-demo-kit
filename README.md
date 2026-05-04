**Informatica CDGC Custom Demo Generator:**

**File:** `cdgc-setup.md`  

**Purpose:** Generate a complete, importable Informatica CDGC demo environment for a customer — 11 Excel files covering every major asset type, ready to bulk-import in order.

---

### Important: CDGC and Data Marketplace setup order

> **Set up CDGC before Data Marketplace** to get full value from both tools. CDGC provides the governance foundation — domains, business terms, policies, and data quality rules — that Data Marketplace surfaces to data consumers. Without CDGC in place, Data Marketplace collections will lack linked glossary terms, certified definitions, and DQ scores.

**Recommended order:**
1. Import CDGC assets using `/cdgc-setup` (this skill)
2. Import Data Marketplace assets using `/marketplace-setup`
3. In CDGC, link Data Sets to Data Collections via the Relationships import
4. In Marketplace, verify that Data Collections surface linked CDGC Business Terms

---

### Important: User-dependent fields

Some import files contain fields that must reference a valid user account in the IDMC org. If these are not updated to match a real user before import, the record will fail or import with an unresolved reference.

| File | Field | Note |
|------|-------|-------|
| `14_Consumer_Access.xlsx` | `Data User` | Must be the email address of an existing Data Marketplace user in the org. The generated files use `woppedisano@informatica.com` as a placeholder — **update this to a valid user email before importing** or the record will fail to resolve. |
| `09_Data_Collection.xlsx` | `Data Owners`, `Technical Owners` | Should be valid org user emails. Generated files use role-based placeholder emails (e.g., `data.engineering@customer.com`) — update if your org enforces user resolution on import. |

**Best practice:** Before importing files 09 and 14, confirm the target user emails exist in your IDMC org under **Administrator → Users**.

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
| 07 | `07_System.xlsx` | System |
| 08 | `08_Business_Term.xlsx` | Business Term |
| 09 | `09_Data_Set.xlsx` | Data Set |
| 10 | `10_DQ_Rule_Template.xlsx` | DQ Rule Template |
| 11 | `11_Relationships.xlsx` | Cross-asset relationships |

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
| Domains | 4 (Customer & KYC, Transactions, General Ledger, Risk & Regulatory) |
| Subdomains | 9 |
| Regulations | 7 (BCBS 239, CCAR, FATCA, BSA/AML, SOX, MiFID II, GDPR) |
| Policies | 5 |
| Systems | 4 (Core Banking, Risk Mgmt Platform, Regulatory Reporting, Data Warehouse) |
| Business Terms | 31 |
| Data Sets | 5 |
| DQ Rule Templates | 10 |
| Relationships | 25 |

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

#### Oil & Gas
Upstream E&P, midstream pipeline, downstream refining, oilfield services, and integrated energy companies.

| Asset Type | Count |
|-----------|-------|
| Domains | 4 (Assets & Operations, HSE & Compliance, Supply Chain & Procurement, Finance & Commercial) |
| Subdomains | 9 |
| Regulations | 7 (BSEE, EPA Clean Air Act, EPA Clean Water Act, PHMSA, OSHA PSM, SEC Reg S-X, EITI) |
| Policies | 5 |
| Systems | 4 (SCADA/Historian, Enterprise Asset Management, Production Accounting, HSE Management) |
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
| Systems | 4 (ERP/MES, Product Lifecycle Management, Quality Management, Supply Chain Planning) |
| Business Terms | 28 |
| Data Sets | 5 |
| DQ Rule Templates | 10 |
| Relationships | 25 |

---

### Import order

Always import in file number order — CDGC validates parent references at import time.

```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11
```

**After importing 08 and 09:** export Business Terms and Data Sets from the CDGC UI to get system-assigned `BT-X` / `DS-X` Reference IDs. Verify or update `11_Relationships.xlsx` with those IDs before importing — mismatched IDs fail silently.

**Import method:** CDGC UI → Gear icon → Import → Upload file → Map columns → Import (one file at a time).

---

### Sharing this skill

**With a colleague:** Send them `cdgc-setup.md`. They save it to `~/.claude/commands/cdgc-setup.md` and type `/cdgc-setup` in any Claude Code session.

**With a team via git:** Add `cdgc-setup.md` to a shared repo under `.claude/commands/cdgc-setup.md` at the repo root. Anyone who clones the repo and opens Claude Code in that directory gets the skill automatically.

**Via plugin marketplace (advanced):** Package with a `plugin.json` manifest and distribute via a private marketplace URL. Team members install with `claude plugin add <marketplace-url>`.
                                                                               
