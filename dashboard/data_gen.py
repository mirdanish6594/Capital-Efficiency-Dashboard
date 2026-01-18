import sqlite3
import pandas as pd
import os

# Database file path
DB_FILE = "financial_db.sqlite"

def create_database():
    # Remove old db if exists to ensure fresh start
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # --- 1. CREATE TABLES ---
    # Products Table (Inventory)
    c.execute('''CREATE TABLE products (
        productCode TEXT PRIMARY KEY,
        productName TEXT,
        productLine TEXT,
        quantityInStock INTEGER,
        buyPrice REAL,
        MSRP REAL
    )''')

    # Customers Table (Risk Analysis)
    c.execute('''CREATE TABLE customers (
        customerNumber INTEGER PRIMARY KEY,
        customerName TEXT,
        country TEXT,
        creditLimit REAL
    )''')

    # Orders Table (Time & Status)
    c.execute('''CREATE TABLE orders (
        orderNumber INTEGER PRIMARY KEY,
        orderDate TEXT,
        status TEXT,
        customerNumber INTEGER,
        FOREIGN KEY(customerNumber) REFERENCES customers(customerNumber)
    )''')

    # OrderDetails Table (Revenue & Margins)
    c.execute('''CREATE TABLE orderdetails (
        orderNumber INTEGER,
        productCode TEXT,
        quantityOrdered INTEGER,
        priceEach REAL,
        FOREIGN KEY(orderNumber) REFERENCES orders(orderNumber),
        FOREIGN KEY(productCode) REFERENCES products(productCode)
    )''')

    # Payments Table (Accounts Receivable)
    c.execute('''CREATE TABLE payments (
        customerNumber INTEGER,
        amount REAL,
        FOREIGN KEY(customerNumber) REFERENCES customers(customerNumber)
    )''')

    # --- 2. INSERT SAMPLE DATA (Based on Mint Classics) ---
    
    # Products Data
    products = [
        ('S10_1678', '1969 Harley Davidson Ultimate Chopper', 'Motorcycles', 7933, 48.81, 95.70),
        ('S10_1949', '1952 Alpine Renault 1300', 'Classic Cars', 7305, 98.58, 214.30),
        ('S10_4962', '1962 Lancia Delta 16V', 'Classic Cars', 6791, 103.42, 147.74),
        ('S12_1666', '1958 Setra Bus', 'Trucks and Buses', 1579, 77.90, 136.67),
        ('S18_2238', '1998 Chrysler Plymouth Prowler', 'Classic Cars', 4724, 101.51, 163.73),
        ('S18_1749', '1917 Grand Touring Sedan', 'Vintage Cars', 2724, 86.70, 170.00),
        ('S18_2581', 'P-51-D Mustang', 'Planes', 992, 49.00, 84.48),
        ('S24_2011', '18th century schooner', 'Ships', 1898, 82.34, 122.89),
        ('S18_3232', '1992 Ferrari 360 Spider red', 'Classic Cars', 8347, 77.90, 169.34),
        ('S24_2840', '1958 Chevy Corvette Limited Edition', 'Classic Cars', 2542, 15.91, 35.36)
    ]
    c.executemany('INSERT INTO products VALUES (?,?,?,?,?,?)', products)

    # Customers Data
    customers = [
        (103, 'Atelier graphique', 'France', 21000.00),
        (112, 'Signal Gift Stores', 'USA', 71800.00),
        (114, 'Australian Collectors, Co.', 'Australia', 117300.00),
        (124, 'Mini Gifts Distributors Ltd.', 'USA', 210500.00),
        (128, 'Blauer See Auto, Co.', 'Germany', 59700.00),
        (141, 'Euro+ Shopping Channel', 'Spain', 227600.00),
        (148, 'Dragon Souveniers, Ltd.', 'Singapore', 103800.00),
        (321, 'Corporate Gift Ideas Co.', 'USA', 105000.00),
        (450, 'The Sharp Gifts Warehouse', 'USA', 77600.00),
        (496, 'Kelly\'s Gift Shop', 'New Zealand', 110000.00)
    ]
    c.executemany('INSERT INTO customers VALUES (?,?,?,?)', customers)

    # Orders Data
    orders = [
        (10100, '2003-01-06', 'Shipped', 363),
        (10101, '2003-01-09', 'Shipped', 128),
        (10103, '2003-01-29', 'Shipped', 121),
        (10104, '2003-01-31', 'Shipped', 141),
        (10127, '2003-06-03', 'Shipped', 148), # Dragon Souveniers
        (10200, '2003-12-01', 'Shipped', 124), # Mini Gifts
        (10250, '2004-05-11', 'Shipped', 450), # Sharp Gifts
        (10300, '2004-10-04', 'Shipped', 128), # Blauer See
        (10400, '2005-04-01', 'Shipped', 450), # Sharp Gifts
        (10419, '2005-05-17', 'Shipped', 141)  # Euro+
    ]
    # Note: We use some dummy customer IDs in orders for customers we didn't explicitly create above, 
    # but for strict integrity we map them to existing ones for this sample.
    orders_clean = [
        (10100, '2003-01-06', 'Shipped', 103),
        (10101, '2003-01-09', 'Shipped', 112),
        (10103, '2003-01-29', 'Shipped', 124),
        (10104, '2003-01-31', 'Shipped', 141),
        (10105, '2003-02-11', 'Shipped', 141),
        (10106, '2003-02-17', 'Shipped', 124),
        (10107, '2003-02-24', 'Shipped', 148),
        (10108, '2003-03-03', 'Shipped', 124),
        (10109, '2003-03-10', 'Shipped', 141),
        (10200, '2003-12-01', 'Shipped', 148)
    ]
    c.executemany('INSERT INTO orders VALUES (?,?,?,?)', orders_clean)

    # Order Details Data (Linking Orders to Products)
    # OrderNum, ProductCode, Qty, PriceEach
    order_details = [
        (10100, 'S18_1749', 30, 136.00),
        (10100, 'S18_2238', 50, 150.00),
        (10101, 'S10_1949', 25, 200.00), 
        (10101, 'S18_2581', 45, 80.00),
        (10103, 'S10_4962', 26, 140.00),
        (10103, 'S12_1666', 42, 130.00),
        (10104, 'S12_1666', 27, 125.00),
        (10104, 'S18_2238', 35, 155.00),
        (10104, 'S24_2840', 20, 34.00),
        (10105, 'S10_1678', 50, 90.00),
        (10105, 'S18_3232', 40, 160.00),
        (10200, 'S24_2011', 35, 120.00),
        (10200, 'S18_2238', 15, 163.00)
    ]
    c.executemany('INSERT INTO orderdetails VALUES (?,?,?,?)', order_details)

    # Payments Data
    # CustomerNum, Amount
    payments = [
        (103, 6066.78),
        (112, 32641.98),
        (124, 111654.40),
        (141, 40206.20),
        (141, 50000.00),
        (148, 10000.00) # Intentionally low payment to show "High Risk" in dashboard
    ]
    c.executemany('INSERT INTO payments VALUES (?,?)', payments)

    conn.commit()
    conn.close()
    print(f"✅ Database created successfully at: {os.path.abspath(DB_FILE)}")

if __name__ == "__main__":
    create_database()