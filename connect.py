import sqlite3
conn = sqlite3.connect("db/food_orders.sqlite",check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL")
conn.row_factory = sqlite3.Row

