# Odoo Ethiopian Accounting & Financial Localization (Odoo 18.0)

A comprehensive Ethiopian Accounting Localization suite for Odoo 18.0 Community, developed according to the regulations of the **Ministry of Revenues (MOR)** and the **Accounting & Auditing Board of Ethiopia (AABE)**.

---

## 🌟 Features Included

1. **10-Digit Ethiopian TIN Validation**:
   - Enforces strict 10-digit numeric TIN validation on customers and vendors (`res.partner`).
2. **Ethiopian Tax Engine**:
   - **VAT 15%** (Standard Sales & Purchases).
   - **VAT 0% Export** (Zero-rated export of goods & services).
   - **VAT Exempt** (Basic foodstuffs, medical, education, finance).
   - **Turnover Tax (TOT)**: 2% on Goods and 10% on Services for non-VAT registered businesses.
   - **Withholding Tax (WHT)**: 2% purchase deduction.
3. **UI-Configurable Rules & Thresholds**:
   - Withholding tax thresholds (Default: 10,000 ETB for goods, 3,000 ETB for services) are configurable under **Settings $\rightarrow$ Accounting**.
   - Tax rates can be modified directly via the UI under **Accounting $\rightarrow$ Configuration $\rightarrow$ Taxes**.

---

## 🚀 Quick Start

### 1. Start PostgreSQL (Docker)
```bash
sudo docker compose up -d
```

### 2. Run Odoo
```bash
./run
```
Open **`http://localhost:8069`** in your browser.

---

## 📁 Repository Structure

```text
├── custom_addons/
│   └── l10n_et_tax/          # Ethiopian Tax, TIN validation & WHT
├── docs/
│   └── ethiopian_accounting_plan.md # 10-day architectural blueprint
├── docker-compose.yml        # PostgreSQL 16 container setup
├── odoo.conf                 # Odoo server configuration
├── run.sh                    # Startup runner script (symlinked to ./run)
└── .gitignore
```
