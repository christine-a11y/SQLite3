This repository contains an end-to-end Data Engineering / ETL (Extract, Transform, Load) pipeline and database architecture designed to clean "noisy" retail operations data and construct a fully integrated relational data infrastructure using Python and SQLite.

## 🛠️ Tech Stack
* **Python 3** — Core programming language.
* **Pandas & NumPy** — For automated data cleaning, structural normalization, and processing missing values.
* **Jupyter Notebooks (`.ipynb`)** — For exploratory data analysis (EDA) and experimental prototyping.
* **SQLite3** — Lightweight relational database engine for operational storage, analytical views, and triggers.

---

## 📋 Project Scope & Implementation

The objective of this project is to take raw, production-noisy CSV datasets (`customers_noisy.csv`, `orders_noisy.csv`, `products_noisy.csv`, `inventory_noisy.csv`) and pass them through an automated cleaning pipeline before uploading them into a clean relational database.

### 1. Data Cleaning Pipelines (Pandas Layer)
* **Customers & Orders Extraction:**
  * Dropped invalid or corrupt identifiers where `CustomerID` or `OrderID` were missing (`NaN`) or set to default junk values like `-1`.
  * Removed incomplete profiles where both `FirstName` and `LastName` were missing simultaneously.
  * Standardized data formats (e.g., lowercased all email records for uniformity).
  * Validated numerical amounts; negative transactions in `OrderAmount` were flagged and cleaned.
  * Categorized order statuses into strict constraints (`Pending`, `Shipped`, `Cancelled`). Any undefined status fallback defaults to `Pending`.
* **Products & Warehouse Inventory:**
  * Cleaned out dummy string values and missing records in product listings.
  * Imputed missing operational stock matrix points with computed statistical averages (`mean`).
  * Enforced relational data integrity by omitting `Inventory` records that referenced non-existent `ProductID` keys.

### 2. Database Architecture (SQLite Layer)
The target destination database structures data into a clean, relational diagram:
* **Products:** `ProductID` (PK), `ProductName`, `Category`, `Price`
* **Inventory:** `InventoryID` (PK), `ProductID` (FK), `WarehouseCode`, `StockLevel`
* **Sales:** `SaleID` (PK), `ProductID` (FK), `QuantitySold`, `SaleDate`
* **Customers:** `CustomerID` (PK), `FirstName`, `LastName`, `Email`, `JoinDate`
* **Orders:** `OrderID` (PK), `CustomerID` (FK), `OrderDate`, `OrderAmount`, `Status`
* **OrderStatusLog:** `LogID` (PK), `OrderID`, `OldStatus`, `NewStatus`, `ChangeDate`

### 3. Database Automation & Analytics
* **`LogOrderStatusChange` Trigger:** An automated database trigger that listens to status updates inside the `Orders` table. It logs any change instantly into the audit table `OrderStatusLog` along with a timestamp.
* **`CustomerRevenueSummary` View:** A reporting view designed for business metrics. It computes total order frequencies per user and measures accumulated financial revenue strictly derived from **"Shipped"** batches.

---

## 📂 Repository Structure

```bash
├── Data/
│   ├── Row/                  # Input datasets with format issues
│   │   ├── customers_noisy.csv
│   │   ├── orders_noisy.csv
│   │   ├── products_noisy (1).csv
│   │   └── inventory_noisy (1).csv
│   └── Processed/            # Sanitized output target data
│       └── customers_clean.csv
├── task.ipynb                # Notebook 1: Products & Inventory pipeline
├── task2.ipynb               # Notebook 2: Views mapping & analytics
├── task3.ipynb               # Notebook 3: Quality controls & structural integrity
├── task4.ipynb               # Notebook 4: Customers & Orders pipelines
├── CustomerOrders.db         # Resulting operational database
├── main.py                   # Master orchestration production ETL script
└── README.md                 # Documentation