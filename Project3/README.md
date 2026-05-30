# Retail System Database Automation

This repository features an automated Python-based ETL (Extract, Transform, Load) pipeline that cleans messy retail data using **Pandas** and structures it into a relational **SQLite** database. It also implements advanced database functionalities like **SQL triggers, views, and complex conditional updates**.

---

## 🚀 Features

* **Data Cleaning:** Dynamically handles missing numeric values using column means.
* **Referential Integrity:** Validates data constraints (ensuring `ProductID` in the inventory dataset exists in the products dataset) before database insertion.
* **Automated Inventory Management:** Uses an SQLite `TRIGGER` to automatically deduct stock levels when a sale is recorded.
* **Business Intelligence View:** Includes a pre-configured `VIEW` to calculate potential revenue by product category.
* **Targeted Promotions:** A complex update query automatically applies a 20% discount to items in specific warehouses with low stock levels.

---

## 📊 Database Schema

The script generates an SQLite database named `RetailSystem.db` consisting of three relational tables: