 ---                                                                                                                                                                                                     
  description: Build and import a full CDGC (Cloud Data Governance & Catalog) demo environment for a financial services customer. Generates all 11 asset type import files in the correct Informatica bulk
   import format.                                                                                                                                                                                         
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  # CDGC Demo Environment Setup                                                                                                                                                                           
                                                                                                                                                                                                          
  You are an Informatica CDGC specialist. Your job is to generate a complete, importable demo environment for a financial services customer using the official Informatica bulk import format.            
                  
  ## What this skill produces                                                                                                                                                                             
                  
  11 Excel files, imported in order, covering every major asset type in CDGC:                                                                                                                             
   
  | # | File | Asset Type | Notes |                                                                                                                                                                       
  |---|------|-----------|-------|
  | 01 | `01_Domain.xlsx` | Domain | Top-level data governance domains |                                                                                                                                  
  | 02 | `02_Subdomain.xlsx` | Subdomain | Must reference parent Domain by `Name \| Reference ID` |                                                                                                       
  | 03 | `03_Regulation.xlsx` | Regulation | Regulatory frameworks (BCBS 239, CCAR, etc.) |                                                                                                               
  | 04 | `04_Policy.xlsx` | Policy | Data governance policies |                                                                                                                                           
  | 05 | `05_Legal_Entity.xlsx` | Legal Entity | Corporate legal entities |                                                                                                                               
  | 06 | `06_Business_Area.xlsx` | Business Area | Organizational units |                                                                                                                                 
  | 07 | `07_System.xlsx` | System | Source/target systems |                                                                                                                                              
  | 08 | `08_Business_Term.xlsx` | Business Term | Glossary terms |                                                                                                                                       
  | 09 | `09_Data_Set.xlsx` | Data Set | Logical data sets |                                                                                                                                              
  | 10 | `10_DQ_Rule_Template.xlsx` | Data Quality Rule Template | DQ rule definitions |                                                                                                                  
  | 11 | `11_Relationships.xlsx` | Relationships | Cross-asset linkages |                                                                                                                                 
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ## Step 1 — Gather customer context                                                                                                                                                                     
                  
  Ask the user for:                                                                                                                                                                                       
                  
  1. **Customer name** (e.g., First Capital Bank) — used to brand the demo data                                                                                                                           
  2. **Industry vertical** (Financial Services, Healthcare, Retail, etc.)
  3. **Key regulatory concerns** (e.g., BCBS 239, GDPR, HIPAA, SOX, FATCA)                                                                                                                                
  4. **Primary data domains** (e.g., Customer, Transactions, Risk — or accept defaults)                                                                                                                   
  5. **Output directory** (default: `~/Downloads/CDGC_Import_<CustomerName>/`)                                                                                                                            
                                                                                                                                                                                                          
  If the user says "use defaults" or provides a customer name only, proceed with the financial services defaults documented below.                                                                        
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                  
  ## Step 2 — Generate the import files                                                                                                                                                                   
   
  Use Python + openpyxl to generate all 11 files. Follow every rule below exactly — CDGC is strict about format.                                                                                          
                  
  ### Universal rules (apply to every sheet)                                                                                                                                                              
                  
  - Sheet name must match exactly (see column specs below)                                                                                                                                                
  - Column order must match the template exactly — CDGC reads positionally
  - `Operation` column must be `Create` for all new records                                                                                                                                               
  - `Lifecycle` must be one of: `Draft`, `In Review`, `Published`, `Obsolete`                                                                                                                             
  - Boolean fields (`Critical Data Element`, `Enable Automation`) must be lowercase: `true` / `false`                                                                                                     
  - Remove all empty sheets before saving — CDGC rejects files with header-only sheets                                                                                                                    
  - Do NOT include an Instructions or Annexure sheet                                                                                                                                                      
  - Reference IDs are optional on create but useful for relationships — use format `DOM-1`, `BT-1`, `POL-1`, etc.                                                                                         
  - Parent references use format `Display Name | Reference ID` (e.g., `Customer & KYC | DOM-5`)                                                                                                           
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ### Sheet specs and column order                                                                                                                                                                        
                  
  #### Domain                                                                                                                                                                                             
  Sheet name: `Domain`
  Columns (in order): `Reference ID`, `Name`, `Description`, `Lifecycle`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`, `Critical Data Element`                  
                                                                                                                                                                                                          
  #### Subdomain                                                                                                                                                                                          
  Sheet name: `Subdomain`                                                                                                                                                                                 
  Columns: `Reference ID`, `Name`, `Description`, `Lifecycle`, `Parent: Domain`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`                                    
  - `Parent: Domain` format: `Domain Name | DOM-X`                                                                                                                                                        
                                                                                                                                                                                                          
  #### Regulation                                                                                                                                                                                         
  Sheet name: `Regulation`                                                                                                                                                                                
  Columns: `Reference ID`, `Name`, `Description`, `Lifecycle`, `Issuing Body`, `Regulation Type`, `Regulation URL`, `Operation`                                                                           
  - `Regulation Type` valid values: `Industry Standard`, `Government Regulation`, `Internal Policy`                                                                                                       
                                                                                                                                                                                                          
  #### Policy                                                                                                                                                                                             
  Sheet name: `Policy`                                                                                                                                                                                    
  Columns: `Reference ID`, `Name`, `Description`, `Lifecycle`, `Policy Type`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`                                       
  - `Policy Type` valid values: `Data Standards`, `Business Rule`, `Technical Standards`, `Conduct Standards`                                                                                             
                                                                                                                                                                                                          
  #### Legal Entity                                                                                                                                                                                       
  Sheet name: `Legal Entity`                                                                                                                                                                              
  Columns: `Reference ID`, `Name`, `Description`, `Lifecycle`, `Operation`                                                                                                                                
                                                                                                                                                                                                          
  #### Business Area                                                                                                                                                                                      
  Sheet name: `Business Area`                                                                                                                                                                             
  Columns: `Reference ID`, `Name`, `Description`, `Lifecycle`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`                                                      
                                                                                                                                                                                                          
  #### System                                                                                                                                                                                             
  Sheet name: `System`                                                                                                                                                                                    
  Columns: `Reference ID`, `Name`, `Description`, `Lifecycle`, `System Type`, `System Purpose`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`                     
  - `System Type` valid value: `Software Application`                                                                                                                                                     
  - `System Purpose` valid values: `Operational`, `Analytical`, `Reporting`, `Integration`, `Master Data Management`                                                                                      
                                                                                                                                                                                                          
  #### Business Term                                                                                                                                                                                      
  Sheet name: `Business Term`                                                                                                                                                                             
  Columns: `Reference ID`, `Name`, `Description`, `Lifecycle`, `Parent: Domain`, `Parent: Business Term`, `Abbreviation`, `Acronym`, `Example`, `Note`, `Critical Data Element`, `Synonym`, `Related      
  Terms`, `Has Policy`, `Has Regulation`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`, `Primary Contact`, `Secondary Contact`                                   
  - `Parent: Domain` format: `Domain Name | DOM-X`                                                                                                                                                        
  - `Critical Data Element`: `true` or `false`                                                                                                                                                            
  - Do NOT populate `Parent: Business Term` — leave blank (causes import failure)                                                                                                                         
  - `Has Policy` / `Has Regulation`: leave blank on initial import (link via Relationships)                                                                                                               
                                                                                                                                                                                                          
  #### Data Set                                                                                                                                                                                           
  Sheet name: `Data Set`                                                                                                                                                                                  
  Columns: `Reference ID`, `Name`, `Description`, `Lifecycle`, `Parent: Domain`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`                                    
  - `Parent: Domain` format: `Domain Name | DOM-X`                                                                                                                                                        
                                                                                                                                                                                                          
  #### Data Quality Rule Template                                                                                                                                                                         
  Sheet name: `Data Quality Rule Template`                                                                                                                                                                
  Columns: `Reference ID`, `Name`, `Description`, `Criticality`, `Dimension`, `Enable Automation`, `Frequency`, `Input Port Name`, `Lifecycle`, `Measuring Method`, `Output Port Name`, `Technical        
  Description`, `Technical Rule Reference`, `Target`, `Threshold`, `Primary Glossary`, `Secondary Glossary`, `Operation`, `Stakeholder: Governance Owner`, `Stakeholder: Governance Administrator`        
  - `Criticality` valid values: `High`, `Medium`, `Low`                                                                                                                                                   
  - `Dimension` valid values: `Accuracy`, `Validity`, `Completeness`, `Consistency`, `Uniqueness`, `Timeliness`                                                                                           
  - `Enable Automation`: `true` or `false`                                                                                                                                                                
  - `Measuring Method` valid values: `BusinessExtract`, `SystemFunction`, `TechnicalScript`, `InformaticaCloudDataQuality`                                                                                
  - `Target` / `Threshold`: numeric values only (e.g., `100`, `0`) — no percent sign                                                                                                                      
  - `Primary Glossary` / `Secondary Glossary`: `Term Name | BT-X` format — **leave blank on first import**, update in a second pass once Business Terms are created and you have their Reference IDs      
                                                                                                                                                                                                          
  #### Relationships                                                                                                                                                                                      
  Sheet name: `Relationships`                                                                                                                                                                             
  Columns: `Source Asset`, `Source Asset Type`, `Target Asset`, `Target Asset Type`, `Relationship Type`, `Operation`                                                                                     
  - All asset references must use Reference IDs (e.g., `POL-1`, `BT-23`) — display names will fail silently                                                                                               
  - Valid relationship types (from Annexure):                                                                                                                                                             
    - Policy → Business Term: `is Regulating`                                                                                                                                                             
    - Policy → Domain: `is Regulating`                                                                                                                                                                    
    - System → Data Set: `is a Strategic Source for`                                                                                                                                                      
    - Data Set → Business Term: `is Defined by`                                                                                                                                                           
    - Business Term → Business Term: `is Related to`, `is Described by`, `is Classified by`                                                                                                               
    - Domain → Subdomain: `is the Parent of`                                                                                                                                                              
  - **Import relationships last** — all referenced assets must exist first                                                                                                                                
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ## Step 3 — Vertical defaults                                                                                                                                                                           
   
  Select the matching vertical based on the customer's industry from Step 1. Adapt all names to the specific customer.                                                                                    
                  
  ---                                                                                                                                                                                                     
                  
  ### Financial Services                                                                                                                                                                                  
                  
  Use for banks, credit unions, capital markets, insurance, and fintech customers.                                                                                                                        
                  
  ### Domains (4)                                                                                                                                                                                         
  - `Customer & KYC` — customer identity, onboarding, KYC compliance
  - `Transactions` — payment transactions, trade settlement                                                                                                                                               
  - `General Ledger` — accounting entries, financial reporting                                                                                                                                            
  - `Risk & Regulatory` — credit risk, market risk, regulatory reporting                                                                                                                                  
                                                                                                                                                                                                          
  ### Subdomains (9)                                                                                                                                                                                      
  - Customer & KYC: Customer Identity, KYC & Compliance, Customer Segmentation                                                                                                                            
  - Transactions: Payment Processing, Trade Settlement                                                                                                                                                    
  - General Ledger: Accounting Entries, Financial Close                                                                                                                                                   
  - Risk & Regulatory: Credit Risk, Regulatory Reporting                                                                                                                                                  
                                                                                                                                                                                                          
  ### Regulations (7)                                                                                                                                                                                     
  BCBS 239, CCAR, FATCA, BSA/AML, SOX, MiFID II, GDPR                                                                                                                                                     
                                                                                                                                                                                                          
  ### Policies (5)                                                                                                                                                                                        
  - Data Quality Standards (Data Standards)                                                                                                                                                               
  - Customer Data Privacy Policy (Conduct Standards)                                                                                                                                                      
  - Regulatory Reporting Policy (Business Rule)                                                                                                                                                           
  - Data Retention Policy (Technical Standards)                                                                                                                                                           
  - GL Reconciliation Policy (Business Rule)                                                                                                                                                              
                                                                                                                                                                                                          
  ### Systems (4)                                                                                                                                                                                         
  - Core Banking System (Operational)                                                                                                                                                                     
  - Risk Management Platform (Analytical)                                                                                                                                                                 
  - Regulatory Reporting System (Reporting)                                                                                                                                                               
  - Data Warehouse (Analytical)                                                                                                                                                                           
                                                                                                                                                                                                          
  ### Data Sets (5)                                                                                                                                                                                       
  - Customer Master (Customer & KYC)                                                                                                                                                                      
  - Transaction History (Transactions)                                                                                                                                                                    
  - GL Entry Register (General Ledger)                                                                                                                                                                    
  - Risk Exposure Data (Risk & Regulatory)                                                                                                                                                                
  - Regulatory Submissions (Risk & Regulatory)                                                                                                                                                            
                                                                                                                                                                                                          
  ### Business Terms — 31 across all 4 domains                                                                                                                                                            
                                                                                                                                                                                                          
  **Customer & KYC:** Customer ID, Social Security Number, Date of Birth, Email Address, Phone Number, KYC Status, Tax Residency Country, Country of Citizenship, Credit Score                            
                  
  **Transactions:** Transaction ID, Transaction Amount, Transaction Type, Transaction Date, Post Date, Currency Code, CTR Flag, Batch ID                                                                  
                  
  **General Ledger:** GL Balance, GL Account Number, Subledger Balance, Debit Amount, Credit Amount, Entry Status                                                                                         
                  
  **Risk & Regulatory:** Capital Ratio, Risk-Weighted Asset, Probability of Default, Loss Given Default, Exposure at Default, BCBS 239 Principle, CCAR, Y-9C Report                                       
                  
  ### DQ Rule Templates (10)                                                                                                                                                                              
  - SSN Not Null (Completeness, High)
  - SSN Format Validity (Validity, High)                                                                                                                                                                  
  - Credit Score Range 300–850 (Validity, High)                                                                                                                                                           
  - Tax Residency Required for Non-US (Completeness, High)                                                                                                                                                
  - Transaction Amount Not Zero (Completeness, High)                                                                                                                                                      
  - Currency Code ISO 4217 (Validity, High)                                                                                                                                                               
  - CTR Flag for Transactions >$10K (Completeness, High)                                                                                                                                                  
  - GL Subledger Balance Match (Consistency, High)                                                                                                                                                        
  - GL Entry Not Zero (Validity, High)                                                                                                                                                                    
  - Debit Credit Balance per Batch (Consistency, High)                                                                                                                                                    
                                                                                                                                                                                                          
  ### Relationships (25)                                                                                                                                                                                  
  - Policy → Business Term `is Regulating`: 8 key linkages                                                                                                                                                
  - Policy → Domain `is Regulating`: 4 (one per domain)                                                                                                                                                   
  - System → Data Set `is a Strategic Source for`: 5                                                                                                                                                      
  - Data Set → Business Term `is Defined by`: 8                                                                                                                                                           
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ### Healthcare                                                                                                                                                                                          
   
  Use for hospitals, health systems, payers, and life sciences customers.                                                                                                                                 
                  
  #### Domains (4)                                                                                                                                                                                        
  - `Patient` — patient identity, demographics, medical history
  - `Clinical` — diagnoses, procedures, medications, lab results                                                                                                                                          
  - `Claims & Billing` — insurance claims, reimbursements, payer data                                                                                                                                     
  - `Compliance & Privacy` — HIPAA, PHI governance, audit trails                                                                                                                                          
                                                                                                                                                                                                          
  #### Subdomains (9)                                                                                                                                                                                     
  - Patient: Patient Identity, Patient Demographics, Medical History                                                                                                                                      
  - Clinical: Diagnoses & Procedures, Medications, Lab Results                                                                                                                                            
  - Claims & Billing: Claims Processing, Payer Management                                                                                                                                                 
  - Compliance & Privacy: PHI Governance, Audit & Reporting                                                                                                                                               
                                                                                                                                                                                                          
  #### Regulations (6)                                                                                                                                                                                    
  HIPAA, HITECH, CMS Conditions of Participation, FDA 21 CFR Part 11, HL7 FHIR, ICD-10                                                                                                                    
                                                                                                                                                                                                          
  #### Policies (5)
  - PHI Data Protection Policy (Conduct Standards)                                                                                                                                                        
  - Data Quality Standards (Data Standards)                                                                                                                                                               
  - Minimum Necessary Use Policy (Business Rule)                                                                                                                                                          
  - Data Retention & Disposal Policy (Technical Standards)                                                                                                                                                
  - Breach Notification Policy (Business Rule)                                                                                                                                                            
                                                                                                                                                                                                          
  #### Systems (4)                                                                                                                                                                                        
  - Electronic Health Record (Operational)                                                                                                                                                                
  - Claims Management System (Operational)
  - Clinical Data Warehouse (Analytical)
  - Regulatory Reporting System (Reporting)
                                                                                                                                                                                                          
  #### Data Sets (5)
  - Patient Master (Patient)                                                                                                                                                                              
  - Clinical Encounters (Clinical)                                                                                                                                                                        
  - Claims Register (Claims & Billing)                                                                                                                                                                    
  - Lab Results (Clinical)                                                                                                                                                                                
  - Compliance Audit Log (Compliance & Privacy)                                                                                                                                                           
                                                                                                                                                                                                          
  #### Business Terms — 28 across all 4 domains                                                                                                                                                           
                                                                                                                                                                                                          
  **Patient:** Patient ID, Medical Record Number (MRN), Date of Birth, Gender, Insurance Member ID, Primary Care Provider, Consent Status                                                                 
                  
  **Clinical:** Diagnosis Code (ICD-10), Procedure Code (CPT), Medication Name, Lab Test Code, Lab Result Value, Encounter Date, Attending Physician                                                      
                  
  **Claims & Billing:** Claim ID, Claim Amount, Payer ID, National Provider Identifier (NPI), Remittance Amount, Denial Reason Code, Service Date                                                         
                  
  **Compliance & Privacy:** PHI Indicator, De-identification Status, Consent Type, Audit Event Type                                                                                                       
                  
  #### DQ Rule Templates (10)                                                                                                                                                                             
  - MRN Not Null (Completeness, High)
  - ICD-10 Code Format Validity (Validity, High)                                                                                                                                                          
  - CPT Code Format Validity (Validity, High)                                                                                                                                                             
  - NPI Format Check (Validity, High)                                                                                                                                                                     
  - Claim Amount Not Zero (Completeness, High)                                                                                                                                                            
  - PHI Flag Required (Completeness, High)                                                                                                                                                                
  - Encounter Date Not Future (Validity, High)                                                                                                                                                            
  - Lab Result Value Range (Validity, Medium)                                                                                                                                                             
  - Consent Status Populated (Completeness, High)                                                                                                                                                         
  - Duplicate Patient Check (Uniqueness, High)                                                                                                                                                            
                                                                                                                                                                                                          
  #### Relationships (25)                                                                                                                                                                                 
  - Policy → Business Term `is Regulating`: 8 key linkages                                                                                                                                                
  - Policy → Domain `is Regulating`: 4 (one per domain)                                                                                                                                                   
  - System → Data Set `is a Strategic Source for`: 5                                                                                                                                                      
  - Data Set → Business Term `is Defined by`: 8                                                                                                                                                           
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ### Retail & CPG                                                                                                                                                                                        
   
  Use for retailers, consumer goods, e-commerce, and grocery customers.                                                                                                                                   
                  
  #### Domains (4)                                                                                                                                                                                        
  - `Customer` — customer identity, loyalty, segmentation
  - `Product` — product catalog, pricing, attributes                                                                                                                                                      
  - `Supply Chain` — inventory, suppliers, logistics                                                                                                                                                      
  - `Transactions` — POS, e-commerce, returns                                                                                                                                                             
                                                                                                                                                                                                          
  #### Subdomains (9)                                                                                                                                                                                     
  - Customer: Customer Identity, Loyalty & Segmentation, Customer Service                                                                                                                                 
  - Product: Product Catalog, Pricing & Promotions                                                                                                                                                        
  - Supply Chain: Inventory Management, Supplier Management                                                                                                                                               
  - Transactions: Point of Sale, E-Commerce, Returns & Refunds                                                                                                                                            
                                                                                                                                                                                                          
  #### Regulations (5)                                                                                                                                                                                    
  GDPR, CCPA, PCI-DSS, California Proposition 65, GS1 Standards                                                                                                                                           
                                                                                                                                                                                                          
  #### Policies (5)                                                                                                                                                                                       
  - Customer Data Privacy Policy (Conduct Standards)                                                                                                                                                      
  - Product Data Standards (Data Standards)                                                                                                                                                               
  - Inventory Accuracy Policy (Business Rule)                                                                                                                                                             
  - PCI Compliance Policy (Technical Standards)                                                                                                                                                           
  - Data Retention Policy (Technical Standards)                                                                                                                                                           
                                                                                                                                                                                                          
  #### Systems (4)                                                                                                                                                                                        
  - Point of Sale System (Operational)                                                                                                                                                                    
  - E-Commerce Platform (Operational)                                                                                                                                                                     
  - ERP / Inventory System (Operational)                                                                                                                                                                  
  - Customer Data Platform (Analytical)                                                                                                                                                                   
                                                                                                                                                                                                          
  #### Data Sets (5)                                                                                                                                                                                      
  - Customer Master (Customer)                                                                                                                                                                            
  - Product Catalog (Product)                                                                                                                                                                             
  - Transaction History (Transactions)                                                                                                                                                                    
  - Inventory Ledger (Supply Chain)                                                                                                                                                                       
  - Supplier Register (Supply Chain)                                                                                                                                                                      
                                                                                                                                                                                                          
  #### Business Terms — 28 across all 4 domains                                                                                                                                                           
                                                                                                                                                                                                          
  **Customer:** Customer ID, Email Address, Loyalty Tier, Customer Lifetime Value, Opt-In Status, Date of Birth, Segment Code                                                                             
                  
  **Product:** SKU, Product Name, Category, Unit Price, UPC Barcode, Brand, Margin                                                                                                                        
                  
  **Supply Chain:** Supplier ID, Lead Time, Reorder Point, Stock on Hand, Purchase Order Number, Warehouse Location                                                                                       
                  
  **Transactions:** Transaction ID, Transaction Amount, Transaction Date, Payment Method, Store ID, Return Flag, Discount Amount                                                                          
                  
  #### DQ Rule Templates (10)                                                                                                                                                                             
  - Customer Email Format (Validity, High)
  - SKU Not Null (Completeness, High)                                                                                                                                                                     
  - UPC Barcode Format (Validity, High)                                                                                                                                                                   
  - Unit Price Not Zero (Completeness, High)                                                                                                                                                              
  - Transaction Amount Not Negative (Validity, High)                                                                                                                                                      
  - Stock on Hand Not Negative (Validity, High)                                                                                                                                                           
  - Duplicate Customer Email (Uniqueness, High)                                                                                                                                                           
  - Lead Time Reasonable Range (Validity, Medium)                                                                                                                                                         
  - Opt-In Status Populated (Completeness, High)                                                                                                                                                          
  - Discount Not Exceed Price (Consistency, High)                                                                                                                                                         
                                                                                                                                                                                                          
  #### Relationships (25)                                                                                                                                                                                 
  - Policy → Business Term `is Regulating`: 8 key linkages                                                                                                                                                
  - Policy → Domain `is Regulating`: 4 (one per domain)                                                                                                                                                   
  - System → Data Set `is a Strategic Source for`: 5                                                                                                                                                      
  - Data Set → Business Term `is Defined by`: 8                                                                                                                                                           
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ### Insurance   

  Use for property & casualty, life, health insurance carriers, reinsurance, and insurance brokerage customers.                                                                                           
   
  #### Domains (4)                                                                                                                                                                                        
  - `Policy & Underwriting` — policy lifecycle, risk assessment, coverage
  - `Claims` — claims intake, adjudication, settlement, fraud                                                                                                                                             
  - `Customer` — policyholder identity, agents, beneficiaries                                                                                                                                             
  - `Risk & Compliance` — actuarial data, regulatory filings, reserving                                                                                                                                   
                                                                                                                                                                                                          
  #### Subdomains (9)                                                                                                                                                                                     
  - Policy & Underwriting: Policy Administration, Underwriting & Rating, Renewals                                                                                                                         
  - Claims: Claims Intake, Claims Adjudication, Fraud Detection                                                                                                                                           
  - Customer: Policyholder Management, Agent & Broker Management                                                                                                                                          
  - Risk & Compliance: Actuarial Reserving, Regulatory Reporting                                                                                                                                          
                                                                                                                                                                                                          
  #### Regulations (7)                                                                                                                                                                                    
  Solvency II, NAIC Model Laws, IFRS 17, State DOI Regulations, GDPR, CCPA, Anti-Money Laundering (AML)                                                                                                   
                                                                                                                                                                                                          
  #### Policies (5)                                                                                                                                                                                       
  - Underwriting Data Quality Standards (Data Standards)                                                                                                                                                  
  - Claims Data Integrity Policy (Business Rule)                                                                                                                                                          
  - Customer Data Privacy Policy (Conduct Standards)                                                                                                                                                      
  - Actuarial Data Standards (Technical Standards)                                                                                                                                                        
  - Regulatory Reporting Policy (Business Rule)                                                                                                                                                           
                                                                                                                                                                                                          
  #### Systems (4)                                                                                                                                                                                        
  - Policy Administration System (Operational)                                                                                                                                                            
  - Claims Management System (Operational)                                                                                                                                                                
  - Actuarial Modeling Platform (Analytical)                                                                                                                                                              
  - Regulatory Reporting System (Reporting)                                                                                                                                                               
                                                                                                                                                                                                          
  #### Data Sets (5)                                                                                                                                                                                      
  - Policyholder Master (Customer)                                                                                                                                                                        
  - Policy Register (Policy & Underwriting)                                                                                                                                                               
  - Claims Register (Claims)                                                                                                                                                                              
  - Actuarial Reserve Data (Risk & Compliance)                                                                                                                                                            
  - Regulatory Submissions (Risk & Compliance)                                                                                                                                                            
                                                                                                                                                                                                          
  #### Business Terms — 28 across all 4 domains                                                                                                                                                           
                                                                                                                                                                                                          
  **Policy & Underwriting:** Policy Number, Coverage Type, Premium Amount, Deductible, Policy Effective Date, Policy Expiration Date, Underwriting Score                                                  
                  
  **Claims:** Claim ID, Claim Date, Claim Amount, Loss Type, Claim Status, Settlement Amount, Fraud Indicator                                                                                             
                  
  **Customer:** Policyholder ID, Date of Birth, Risk Profile, Agent ID, Beneficiary Name, Contact Preference, KYC Status                                                                                  
                  
  **Risk & Compliance:** Loss Ratio, Combined Ratio, Actuarial Reserve Amount, Solvency Capital Requirement, Reinsurance Treaty ID, Regulatory Filing Date, Risk Classification                           
                  
  #### DQ Rule Templates (10)                                                                                                                                                                             
  - Policy Number Not Null (Completeness, High)
  - Premium Amount Not Zero (Completeness, High)                                                                                                                                                          
  - Policy Date Range Valid (Validity, High)                                                                                                                                                              
  - Claim Amount Not Negative (Validity, High)                                                                                                                                                            
  - Loss Ratio Range Check (Validity, High)                                                                                                                                                               
  - Fraud Indicator Populated (Completeness, High)                                                                                                                                                        
  - Deductible Not Exceed Coverage (Consistency, High)                                                                                                                                                    
  - Policyholder DOB Not Future (Validity, High)                                                                                                                                                          
  - Duplicate Claim Check (Uniqueness, High)                                                                                                                                                              
  - Reserve Amount Not Negative (Validity, High)                                                                                                                                                          
                                                                                                                                                                                                          
  #### Relationships (25)                                                                                                                                                                                 
  - Policy → Business Term `is Regulating`: 8 key linkages                                                                                                                                                
  - Policy → Domain `is Regulating`: 4 (one per domain)                                                                                                                                                   
  - System → Data Set `is a Strategic Source for`: 5                                                                                                                                                      
  - Data Set → Business Term `is Defined by`: 8                                                                                                                                                           
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ### Public Sector & Government                                                                                                                                                                          
   
  Use for federal, state, and local government agencies, defense, and public utilities customers.                                                                                                         
                  
  #### Domains (4)                                                                                                                                                                                        
  - `Citizen Services` — citizen identity, benefits, case management
  - `Program & Operations` — grants, contracts, agency programs                                                                                                                                           
  - `Financial Management` — appropriations, expenditures, audit                                                                                                                                          
  - `Compliance & Reporting` — regulatory filings, oversight, FOIA                                                                                                                                        
                                                                                                                                                                                                          
  #### Subdomains (9)                                                                                                                                                                                     
  - Citizen Services: Citizen Identity, Benefits Administration, Case Management                                                                                                                          
  - Program & Operations: Grants Management, Contract Management                                                                                                                                          
  - Financial Management: Budget & Appropriations, Expenditure Tracking                                                                                                                                   
  - Compliance & Reporting: Regulatory Reporting, Audit & Oversight                                                                                                                                       
                                                                                                                                                                                                          
  #### Regulations (7)                                                                                                                                                                                    
  FISMA, FedRAMP, OMB Circular A-123, NIST SP 800-53, Privacy Act of 1974, FOIA, ATO (Authority to Operate)                                                                                               
                                                                                                                                                                                                          
  #### Policies (5)                                                                                                                                                                                       
  - Data Quality Standards (Data Standards)                                                                                                                                                               
  - Personally Identifiable Information (PII) Policy (Conduct Standards)                                                                                                                                  
  - Records Retention Policy (Technical Standards)                                                                                                                                                        
  - Federal Reporting Compliance Policy (Business Rule)                                                                                                                                                   
  - Data Access & Classification Policy (Technical Standards)                                                                                                                                             
                                                                                                                                                                                                          
  #### Systems (4)                                                                                                                                                                                        
  - Case Management System (Operational)                                                                                                                                                                  
  - Financial Management System (Operational)                                                                                                                                                             
  - Grants Management System (Operational)                                                                                                                                                                
  - Data Analytics Platform (Analytical)                                                                                                                                                                  
                                                                                                                                                                                                          
  #### Data Sets (5)                                                                                                                                                                                      
  - Citizen Registry (Citizen Services)                                                                                                                                                                   
  - Benefits Register (Citizen Services)                                                                                                                                                                  
  - General Ledger (Financial Management)                                                                                                                                                                 
  - Grants & Contracts Register (Program & Operations)                                                                                                                                                    
  - Compliance Submissions (Compliance & Reporting)                                                                                                                                                       
                                                                                                                                                                                                          
  #### Business Terms — 28 across all 4 domains                                                                                                                                                           
                                                                                                                                                                                                          
  **Citizen Services:** Citizen ID, Social Security Number, Benefits Eligibility Status, Case ID, Case Worker ID, Program Enrollment Date, Benefit Amount                                                 
                  
                                                                                                                                                                                                          
  **Financial Management:** Appropriation Code, Object Class Code, Obligation Amount, Expenditure Amount, Fund Code, Fiscal Year, Budget Authority
                                                                                                                                                                                                          
  **Compliance & Reporting:** FOIA Request ID, Audit Finding, Compliance Status, Report Submission Date, Classification Level, PII Indicator
                                                                                                                                                                                                          
  #### DQ Rule Templates (10)
  - Citizen ID Not Null (Completeness, High)                                                                                                                                                              
  - SSN Format Validity (Validity, High)    
  - Benefits Eligibility Status Valid (Validity, High)                                                                                                                                                    
  - Obligation Amount Not Negative (Validity, High)                                                                                                                                                       
  - Expenditure Not Exceed Appropriation (Consistency, High)                                                                                                                                              
  - Grant Award Amount Not Zero (Completeness, High)                                                                                                                                                      
  - PII Indicator Required (Completeness, High)                                                                                                                                                           
  - Fiscal Year Format Valid (Validity, High)                                                                                                                                                             
  - Compliance Status Populated (Completeness, High)                                                                                                                                                      
  - Duplicate Citizen Record Check (Uniqueness, High)                                                                                                                                                     
                                                                                                                                                                                                          
  #### Relationships (25)                                                                                                                                                                                 
  - Policy → Business Term `is Regulating`: 8 key linkages                                                                                                                                                
  - Policy → Domain `is Regulating`: 4 (one per domain)                                                                                                                                                   
  - System → Data Set `is a Strategic Source for`: 5                                                                                                                                                      
  - Data Set → Business Term `is Defined by`: 8                                                                                                                                                           
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ## Step 4 — Import order and instructions                                                                                                                                                               
                                                                                                                                                                                                          
  Tell the user to import files in this exact order:
                                                                                                                                                                                                          
  01_Domain.xlsx          ← no dependencies
  02_Subdomain.xlsx       ← depends on Domains                                                                                                                                                            
  03_Regulation.xlsx      ← no dependencies                                                                                                                                                               
  04_Policy.xlsx          ← no dependencies                                                                                                                                                               
  05_Legal_Entity.xlsx    ← no dependencies                                                                                                                                                               
  06_Business_Area.xlsx   ← no dependencies                                                                                                                                                               
  07_System.xlsx          ← no dependencies                                                                                                                                                               
  08_Business_Term.xlsx   ← depends on Domains                                                                                                                                                            
  09_Data_Set.xlsx        ← depends on Domains                                                                                                                                                            
  10_DQ_Rule_Template.xlsx ← standalone (link glossary after export)                                                                                                                                      
  11_Relationships.xlsx   ← depends on ALL above                                                                                                                                                          
                                                                                                                                                                                                          
  **Import method:** CDGC UI → Gear icon → Import → Upload file → Map columns (auto-maps if headers match) → Import                                                                                       
                                                                                                                                                                                                          
  **One file at a time** — do not combine sheets into one workbook for import.                                                                                                                            
                                                                                                                                                                                                          
  **After importing 08 and 09**, export Business Terms and Data Sets to get their system-assigned Reference IDs (BT-X, DS-X). Use those IDs to build the Relationships file.                              
                  
  **After importing 10**, export DQ Rule Templates to get DQR-X Reference IDs if needed.                                                                                                                  
                  
  ---                                                                                                                                                                                                     
                  
  ## Step 5 — Confirmation checklist                                                                                                                                                                      
                  
  After all imports, verify in the CDGC UI:                                                                                                                                                               
                  
  - [ ] Glossary tab shows 4 Domains with nested Subdomains                                                                                                                                               
  - [ ] Business Terms visible under each Domain (31 total)
  - [ ] Policies (5) visible in Glossary                                                                                                                                                                  
  - [ ] Regulations (7) visible in Glossary                                                                                                                                                               
  - [ ] Systems (4) visible in Glossary                                                                                                                                                                   
  - [ ] Data Sets (5) visible in Glossary                                                                                                                                                                 
  - [ ] DQ Rule Templates (10) — search by name to confirm                                                                                                                                                
  - [ ] Relationships: open a Policy → Relationships tab → should show linked Business Terms                                                                                                              
  - [ ] Relationships: open a System → Relationships tab → should show linked Data Sets                                                                                                                   
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ## Common errors and fixes                                                                                                                                                                              
   
  | Error | Fix |                                                                                                                                                                                         
  |-------|-----| 
  | `Enter a valid value from [Create, Update, Delete]` | Operation column missing or wrong position |                                                                                                    
  | `The parent is invalid or not present` | Parent asset doesn't exist yet — import Domains first |                                                                                                      
  | `Imported file contains empty values` | Remove header-only sheets from the workbook |                                                                                                                 
  | Pre-validation failure | Remove Instructions/Annexure sheets |                                                                                                                                        
  | Business Terms not visible after import | Remove `Parent: Subdomain` column — use `Parent: Domain` only |                                                                                             
  | `Parent already exists` on Relationships | Relationship already created in a prior import — not an error |                                                                                            
  | DQ Rule Template score not showing on Business Term | Expected — scores only appear after a live DQ scan against a connected source |                                                                 
  | Policy Type / System Type invalid value | Check valid values in column specs above |                                                                                                                  
  | Relationship fails silently | Must use Reference IDs (e.g., `BT-23`), not display names |                                                                                                             
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                     
                                                                                                                                                                                                          
  ## Sharing this skill                                                                                                                                                                                   
   
  This skill is a Markdown file at `~/.claude/commands/cdgc-setup.md`.                                                                                                                                    
                  
  **To share with a colleague:**                                                                                                                                                                          
  1. Send them the file — they save it to `~/.claude/commands/cdgc-setup.md` on their machine
  2. They type `/cdgc-setup` in any Claude Code session to invoke it                                                                                                                                      
                                                                                                                                                                                                          
  **To publish to a team:**                                                                                                                                                                               
  - Add the file to a shared git repo under `.claude/commands/cdgc-setup.md` at the repo root                                                                                                             
  - Anyone who clones the repo and opens Claude Code in that directory gets the skill automatically                                                                                                       
  - This is the recommended approach for Salesforce team / partner enablement                                                                                                                             
                                                                                                                                                                                                          
  **To publish to a plugin marketplace** (advanced):                                                                                                                                                      
  - Package as a Claude Code plugin with a `plugin.json` manifest                                                                                                                                         
  - Distribute via a private marketplace URL                                                                                                                                                              
  - Team members install via `claude plugin add <marketplace-url>`                                                                                                                                        
                                                                                                                                                                                                          
  ---                                                                                                                                                                                                                                                                                                                                     
  ---  
