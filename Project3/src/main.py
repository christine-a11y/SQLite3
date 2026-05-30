import pandas as pd
import sqlite3
import os

# Paths
data_dir = os.path.join(os.path.dirname(__file__), '..', 'Data')
products_csv = os.path.join(data_dir, 'products_raw.csv')
inventory_csv = os.path.join(data_dir, 'inventory_levels.csv')
db_path = os.path.join(data_dir, 'RetailSystem.db')

# Part 1: Data Cleaning
# Load products
products_df = pd.read_csv(products_csv)
print("Products Data:")
print(products_df.head())

# Fill missing Price with mean
products_df['Price'] = products_df['Price'].fillna(products_df['Price'].mean())

print("After filling missing Price:")
print(products_df)

# Load inventory
inventory_df = pd.read_csv(inventory_csv)
print("\nInventory Data:")
print(inventory_df.head())

# Fill missing StockLevel with median
inventory_df['StockLevel'] = inventory_df['StockLevel'].fillna(inventory_df['StockLevel'].median())

print("After filling missing StockLevel:")
print(inventory_df)

# Validation: Ensure every ProductID in inventory exists in products
products_ids = set(products_df['ProductID'])
inventory_ids = set(inventory_df['ProductID'])
missing_ids = inventory_ids - products_ids
if missing_ids:
    print(f"Warning: ProductIDs in inventory not in products: {missing_ids}")
    # Filter out invalid inventory entries
    inventory_df = inventory_df[inventory_df['ProductID'].isin(products_ids)]
    print("Filtered inventory to valid ProductIDs")

# Part 2: Database Design
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    ProductID INTEGER PRIMARY KEY,
    ProductName TEXT,
    Category TEXT,
    Price REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Inventory (
    InventoryID INTEGER PRIMARY KEY,
    ProductID INTEGER,
    WarehouseCode TEXT,
    StockLevel INTEGER,
    FOREIGN KEY (ProductID) REFERENCES Products (ProductID)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Sales (
    SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductID INTEGER,
    QuantitySold INTEGER,
    SaleDate TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ProductID) REFERENCES Products (ProductID)
)
''')

conn.commit()

# Part 3: Insert data
# Insert Products
products_df.to_sql('Products', conn, if_exists='replace', index=False)

# Insert Inventory
inventory_df.to_sql('Inventory', conn, if_exists='replace', index=False)

print("\nData inserted successfully.")

# Close connection
conn.close()