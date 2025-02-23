import sqlite3
conn = sqlite3.connect("db/food_orders.sqlite",check_same_thread=False)
conn.row_factory = sqlite3.Row

def conn_to_write():
    wconn = sqlite3.connect("db/food_orders.sqlite")
    wconn.execute("PRAGMA journal_mode=WAL")
    return  wconn
