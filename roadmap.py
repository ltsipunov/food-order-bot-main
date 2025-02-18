# from connect import conn
#
# select_categories_query = '''
# SELECT id,name FROM categories WHERE restaurant_id=?
# '''
# select_dishes_query = '''
# SELECT id,name,price FROM dishes WHERE category_id=?
# '''
#
# insert_review_query = '''
# INSERT INTO reviews (user_id, restaurant_id, order_id,  rating, comment)
# VALUES (?,?,?,?,?)
# '''


class RoadMap:
    def __init__(self,u_id=1,r_id=1):
        self.user_id = u_id
        self.restaurant_id = r_id
        self.category_id =  None
        self.dish_id = None
    # def add_review(self,order_id,rate,text):
    #     cursor = conn.cursor()
    #     cursor.
    #     cursor.execute(insert_review_query, (self.user_id,self.restaurant_id,order_id,text ))
    #     rows = cursor.fetchall()
    #     cursor.close()

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

    def select_resturant(self,r_id):
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
