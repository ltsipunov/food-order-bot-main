import telebot
from dotenv import load_dotenv
import os
from prettytable import PrettyTable

from cart import Cart
from roadmap import RoadMap

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
TEMP = os.getenv("TEMP")
bot = telebot.TeleBot(TOKEN)

roadmap = RoadMap()
cart = Cart(roadmap)

def send_list(bot,from_user,lst,header=[], top=[]):
    table = PrettyTable()
    if header: table.field_names = header
    table.add_rows(lst)
    bot.send_message(from_user.id,f'<pre>{top}\n{table}</pre>',parse_mode='HTML')

@bot.message_handler(commands=["reviews",'W'])
def handle_reviews(message):
    tags = message.text.split(' ')
    if len(tags) >= 1 :
        restaurants_id = int(tags[1])
        send_list(bot, message.from_user, roadmap.all_reviews(restaurants_id),
                  ["Дата", 'Оценка','Отзыв','Автор'],f"Отзывы о ресторане {restaurants_id }" )
    else:
        bot.send_message(message.from_user.id, f'Нераспознаны параметры ресторана')

@bot.message_handler(commands=["review",'V'])
def handle_review(message):
    tags = message.text.split(' ')
    if len(tags) >= 3 :
        order_id = int(tags[1])
        rate= int(tags[2])
        if len(tags)>= 4: text = ' '.join(tags[3:])
        else: text=''
        roadmap.add_review(order_id,rate,text)
    else:
        bot.send_message(message.from_user.id, f'Нераспознаны параметры отзыва')

@bot.message_handler(commands=["payment",'P'])
def handle_payment(message):
    tags = message.text.split(' ')
    if len(tags) > 1 and tags[1] in ['cash','online']:
        cart.set_payment(tags[1])
        desc = f"Установлен метод платежа {cart.payment_method}"
        bot.send_message(message.from_user.id, f'<pre>{desc}</pre>', parse_mode='HTML')
    else:
        bot.send_message(message.from_user.id, f'Нераспознана команда платежа')

@bot.message_handler(commands=["history",'H'])
def handle_history(message):
    send_list(bot, message.from_user, cart.load_history(roadmap.user_id), ["ID", 'Описание'], roadmap.description())

@bot.message_handler(commands=["load",'L'])
def handle_repeat(message):
    tags = message.text.split(' ')
    if len(tags) > 1:
        t = int(tags[1])
        cart.load_order(t)

@bot.message_handler(commands=["drop",'D'])
def handle_drop(message):
    tags = message.text.split(' ')
    if len(tags) > 1:
        t = int(tags[1])
        cart.drop_item(t)
        bot.send_message(message.from_user.id, f'<pre>{cart.item_state(t)}</pre>', parse_mode='HTML')
    else:
        bot.send_message(message.from_user.id,f"Формат команды: '/drop <id блюда>' ")

@bot.message_handler(commands=["cart",'C'])
def handle_cart(message):
    desc = roadmap.description() +'\nПлатёж: ' + cart.payment_method
    if len(cart.items) > 0 :
        send_list(bot, message.from_user, cart.content(), ["ID", 'Блюдо', 'Цена', 'Количество'], desc)
    else:
        bot.send_message(message.from_user.id,f"Корзина пуста ")

@bot.message_handler(commands=["confirm",'F'])
def handle_confirm(message):
    if len(cart.items) > 0 :
        cart.confirm()
        bot.send_message(message.from_user.id,f'<pre>Заказ сохранен</pre>',parse_mode='HTML')
    else:
        bot.send_message(message.from_user.id,f"Корзина пуста ")

@bot.message_handler(commands=["add",'A'])
def handle_add(message):
    tags = message.text.split(' ')
    if len(tags)>1 :
        t = int(tags[1])
        cart.add_item(t)
        bot.send_message(message.from_user.id,f'<pre>{cart.item_state(t)}</pre>',parse_mode='HTML')
    else:
        bot.send_message(message.from_user.id,f"Формат команды: '/add <id блюда>' ")

@bot.message_handler(commands=["restaurant",'R'])
def handle_restaurant(message):
    tags = message.text.split(' ')
    if len(tags)>1 :   t = int(tags[1])
    if not t : t = roadmap.restaurant_id
    if t:   roadmap.select_resturant(t)
    send_list(bot,message.from_user,roadmap.get_categories(), ["ID", 'Категория меню'],roadmap.description() )

@bot.message_handler(commands=["section",'C'])
def handle_section(message):
    # username = message.from_user.first_name
    tags = message.text.split(' ')
    if len(tags)>1 :   t = int(tags[1])
    if not t : t = roadmap.category_id
    if t:   roadmap.select_category(t)
    send_list(bot,message.from_user,roadmap.get_dishes(), ["ID", "Блюда",'Цена'],roadmap.description() )

bot.polling(none_stop=True)
