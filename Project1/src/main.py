import pandas as pd
import sqlite3
import numpy as np

# Read the CSV files
inventory = pd.read_csv("../Data/Row/inventory_noisy (1).csv")
products = pd.read_csv("../Data/Row/products_noisy (1).csv")

# Clean the products dataframe
# Replace -1 with NaN in ProductName (assuming it's a placeholder for missing values)
products['ProductName'] = products['ProductName'].replace(-1, np.nan)
# Fill NaN values in numeric columns with mean
products = products.fillna(products.mean(numeric_only=True))

# Clean the inventory dataframe
# Fill NaN values in numeric columns with mean
inventory = inventory.fillna(inventory.mean(numeric_only=True))

# Filter inventory to only include valid ProductIDs that exist in products
valid_prodID = inventory['ProductID'].isin(products['ProductID'])
inventory = inventory[valid_prodID]

# Create the database
conn = sqlite3.connect("../RetailSystem.db")
cursor = conn.cursor()

# Create tables
cursor.executescript("""
    DROP TABLE IF EXISTS Sales;
    DROP TABLE IF EXISTS Inventory;
    DROP TABLE IF EXISTS Products;

    CREATE TABLE Products (
        ProductID INTEGER PRIMARY KEY,
        ProductName TEXT,
        Category TEXT,
        Price REAL
    );

    CREATE TABLE Inventory (
        InventoryID INTEGER PRIMARY KEY,
        ProductID INTEGER,
        WarehouseCode TEXT,
        StockLevel INTEGER,
        FOREIGN KEY(ProductID) REFERENCES Products(ProductID)
    );

    CREATE TABLE Sales (
        SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
        ProductID INTEGER,
        QuantitySold INTEGER,
        SaleDate TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(ProductID) REFERENCES Products(ProductID)
    );
""")

# Insert data into Products table
products.to_sql('Products', conn, if_exists='replace', index=False)

# Insert data into Inventory table
inventory.to_sql('Inventory', conn, if_exists='replace', index=False)

# Commit and close
conn.commit()
conn.close()

print("Database created and data inserted successfully.")
