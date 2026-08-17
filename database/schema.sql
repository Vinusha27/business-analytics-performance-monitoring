PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY, customer_name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, signup_date TEXT NOT NULL, region TEXT NOT NULL, customer_segment TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL, subcategory TEXT NOT NULL, unit_price REAL NOT NULL CHECK(unit_price >= 0), cost REAL NOT NULL CHECK(cost >= 0), launch_date TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sales_reps (sales_rep_id INTEGER PRIMARY KEY, sales_rep_name TEXT NOT NULL, region TEXT NOT NULL, team TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id), order_date TEXT NOT NULL, region TEXT NOT NULL, sales_channel TEXT NOT NULL, sales_rep_id INTEGER NOT NULL REFERENCES sales_reps(sales_rep_id), order_status TEXT NOT NULL CHECK(order_status IN ('completed','cancelled','returned')));
CREATE TABLE IF NOT EXISTS order_items (order_item_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(order_id), product_id INTEGER NOT NULL REFERENCES products(product_id), quantity INTEGER NOT NULL CHECK(quantity > 0), unit_price REAL NOT NULL CHECK(unit_price >= 0), discount REAL NOT NULL CHECK(discount BETWEEN 0 AND 1));
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_region ON orders(region);
CREATE INDEX IF NOT EXISTS idx_items_product ON order_items(product_id);
