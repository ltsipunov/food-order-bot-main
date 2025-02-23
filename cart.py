from connect import conn,conn_to_write

insert_order_query = '''
INSERT INTO orders (user_id, restaurant_id, status, payment_method, total_cost)
VALUES (?, ?, ?, ?, ?)
'''
insert_order_item_query = '''
INSERT INTO order_items (order_id, dish_id, quantity, price, total)
VALUES (?, ?, ?, ?, ?)
'''

select_order_query = '''
    SELECT restaurant_id,payment_method FROM orders where id = ?  
'''
select_items_query = '''
  SELECT dish_id id,name,oi.price,quantity 
  FROM order_items oi
  JOIN dishes d ON d.id = oi.dish_id 
  WHERE order_id = ?
'''

select_history_query = '''
  SELECT order_id, group_concat(format('%s*%s', name,oi.quantity),' ') description
  FROM orders o 
  JOIN order_items oi ON oi.order_id = o.id
  JOIN dishes d ON d.id = oi.dish_id 
  WHERE user_id = ?
  GROUP BY order_id
'''

def get_dish(dish_id):
    # conn.row_factory= sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f'SELECT id,name,price FROM dishes WHERE id=? ',(dish_id,))
    rows = [ dict(r) for r in cursor.fetchall() ]
    cursor.close()
    return rows

class Cart:
    def __init__(self,  roadmap ,pm='cash' ):
        self.user_id,self.restaurant_id = roadmap.user_id,roadmap.restaurant_id
        self.payment_method = pm
        self.reset()
    def reset(self):
        self.status,self.total_cost,self.items = 'cart',0,[]
    def add_item(self,item_id):
        ids = [ it['id'] for it in self.items ]
        if item_id in ids:
            idx =  ids.index(item_id)
            self.items[idx]['quantity'] += 1
        else:
            ds = get_dish(item_id)
            for d in ds:  d['quantity'] = 1
            self.items += ds
    def drop_item(self,item_id):
        ids = [it['id'] for it in self.items]
        if item_id in ids:
            idx = ids.index(item_id)
            self.items[idx]['quantity'] -= 1
            if self.items[idx]['quantity']==0:  self.items.pop(idx)

    def load_order(self,order_id):
        self.reset()
        cursor=conn.cursor()
        cursor.execute(select_order_query, (order_id,) )
        o =  [ dict(r) for r in cursor.fetchall() ]
        print(o)
        if o :
            self.payment_method = o[0]['payment_method']
            cursor.execute(select_items_query, (order_id,) )
            self.items = [ dict(r) for r in cursor.fetchall() ]
        cursor.close()

    def load_history(self,user_id):
        cursor = conn.cursor()
        cursor.execute(select_history_query, (user_id,) )
        rows= cursor.fetchall()
        print(rows)
        cursor.close()
        return rows
    def set_payment(self,string):
        self.payment_method = string

    def content(self):
        return [  [ it['id'],it['name'],it['price'],it['quantity']] for it in self.items ]
    def item_state(self,id):
        found = [ it for it in self.content() if it[0]==id ]
        if found :
            return f"В корзине #{found[0][0]} {found[0][1]} {found[0][3]} шт по {found[0][2]}"
        else:
            return f" В корзине 0 шт #{id}"

    def confirm(self):
        self.total_cost = sum(item['price'] * item['quantity'] for item in self.items)

        wconn=conn_to_write()
        wcursor =wconn.cursor()
        wcursor.execute(insert_order_query, (
        self.user_id, self.restaurant_id, self.status, self.payment_method, self.total_cost))
        last_order_id = wcursor.lastrowid
        for item in self.items:
            wcursor.execute(insert_order_item_query, (
            last_order_id, item['id'], item['quantity'], item['price'], item['quantity'] * item['price']))
        wconn.commit()
        wcursor.close()
        wconn.close()

        self.reset()