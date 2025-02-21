from connect import conn

select_categories_query = '''
SELECT id,name FROM categories WHERE restaurant_id=?
'''
select_dishes_query = '''
SELECT id,name,price FROM dishes WHERE category_id=?
'''
ask_for_review_query = '''
select restaurant_id  from orders
 where  id = ? 
'''
insert_review_query = '''
insert into reviews (user_id,restaurant_id,order_id,rating,comment) 
values(?,?,?,?,?) 
'''
all_reviews_query = '''
 select date(v.created_at) , rating,comment,u.username   from reviews v  join users u on user_id = u.id 
  where restaurant_id = ?
  order by 1 desc
'''

class RoadMap:
    def __init__(self,u_id=1,r_id=1):
        self.user_id = u_id
        self.restaurant_id = r_id
        self.category_id =  None
        self.dish_id = None

    def all_reviews(self,restaurant_id):
        cursor = conn.cursor()
        cursor.execute(all_reviews_query,(restaurant_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def add_review(self,order_id,rate,text):
        import sqlite3
        conn1 = sqlite3.connect("db/food_orders.sqlite")
        conn1.execute("PRAGMA journal_mode=WAL")

        with cursor = conn.cursor()
            cursor.execute(ask_for_review_query,(order_id,))
            rows=cursor.fetchall()
            cursor.close()
            if rows:
                cursor1 = conn1.cursor()
                try:
                    r_id = dict(rows[0])['restaurant_id']
                    print((self.user_id, r_id,order_id,rate,text, ))
                    cursor1.execute(insert_review_query,(self.user_id, r_id,order_id,rate,text, ))
                    conn1.commit()
                finally:
                    cursor1.close()
            conn1.close()

    def get_categories(self):
        cursor = conn.cursor()
        cursor.execute(select_categories_query, (self.restaurant_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_dishes(self):
        cursor= conn.cursor( )
        cursor.execute(select_dishes_query,(self.category_id,))
        rows=cursor.fetchall()
        cursor.close()
        return rows

    def select_restaurant(self,r_id):
        self.restaurant_id = r_id
        self.category_id = None
        return self.get_categories()

    def select_category(self,cat_id):
        self.category_id = cat_id
        return self.get_dishes()

    def description(self):
        desc=  f"Клиент {self.user_id} в ресторане {self.restaurant_id} "
        if self.category_id: desc += "\n"+ f"Раздел меню {self.category_id}"
        return desc
