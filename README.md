# Ethiopian ERP Suite for Odoo (Odoo 18.0)

A comprehensive, enterprise-grade **Ethiopian ERP Localization & Business Suite** built for Odoo 18.0. 

This repository houses a modular suite of Ethiopian business modules complying with the regulations of the **Ministry of Revenues (MOR)**, the **Accounting & Auditing Board of Ethiopia (AABE)**, and the **Federal Income Tax Proclamation No. 979/2016**.

---

## 📦 Planned & Active Modules (The 5-Module Suite)

| Module | Name | Purpose | Status |
| :--- | :--- | :--- | :---: |
| **`l10n_et_tax`** | Ethiopian Tax & TIN Foundation | 10-digit TIN validation, 15% VAT, 2%/10% TOT, automated 2% WHT deduction & official MOR WHT certificate. | 🚀 Active |
| **`l10n_et_vouchers`** | Ethiopian Financial Vouchers | Cash Payment (CPV), Cash Receipt (CRV), Bank Payment (BPV), Petty Cash (PCV), 4-stage approval workflow & Amharic amount-in-words. | 🚀 Active |
| **`l10n_et_calendar`** | Ethiopian (Ge'ez) Calendar | 13-month calendar engine, Hamle 1 – Sene 30 fiscal year, and dual-date (GC + EC) display on invoices and vouchers. | 📋 Planned |
| **`l10n_et_payroll`** | Ethiopian Payroll & PIT | Employment Income Tax progressive brackets (0% - 35%), 7% employee + 11% employer pension (18% total), and POPSA reporting. | 📋 Planned |
| **`l10n_et_inventory`** | Ethiopian Store Documents | Goods Receiving Note (GRN), Store Issue Voucher (SIV), Store Return Voucher (SRV), and bin card controls. | 📋 Planned |

---

## 🌟 Key Architecture Principles

1. **100% UI-Configurable Rules**: Tax percentages, withholding thresholds (10k goods / 3k services), and accounting accounts are editable from the UI without touching code.
2. **Solid Invariants**: Fixed statutory rules (such as 10-digit numeric TIN length) are strictly enforced in Python constraints.
3. **Clean Modular Structure**: Independent addons in `custom_addons/` that can be installed together or separately.

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
Access the system at **`http://localhost:8069`**.

---

## 📁 Repository Structure

```text
├── custom_addons/
│   ├── l10n_et_tax/          # Tax, TIN validation & Withholding Tax
│   ├── l10n_et_vouchers/     # Financial Vouchers (CPV, CRV, BPV, PCV)
│   ├── l10n_et_calendar/     # 13-Month Ethiopian Ge'ez Calendar
│   ├── l10n_et_payroll/      # Payroll, PIT (0-35%) & 18% Pension
│   └── l10n_et_inventory/    # Store Issue & Goods Receiving (SIV / GRN)
├── docs/
│   └── ethiopian_accounting_plan.md # 10-day implementation roadmap
├── docker-compose.yml        # PostgreSQL 16 container setup
├── odoo.conf                 # Odoo server configuration
├── run.sh                    # Startup runner script (symlinked to ./run)
└── .gitignore
```
