import telebot
import requests
import database

bot = telebot.TeleBot("5655507116:AAEHpo2jyXYfQiTENRkc_2tZqFeRJRjfEWs")

api_key = '23b87d6edd604dd8b7ea8c17a8f1be6a'

# @bot.message_handler(content_types=['text'])
# def hello(message):
#     if message.text == 'Привет':
#         bot.send_message(message.chat.id, "Здравствуйте. Выберите команду:\n/sub - подписка\n/outsub - отписка\n/news - новости")

def converting(news):
    str = ''
    for i in news:
        str += i+"\n"
    return str

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, " + message.from_user.first_name)
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    useReg = database.user_prov(us_id)
    if (useReg == None):
        database.users_db(id_user=us_id, user_name=us_name)
        bot.send_message(message.chat.id, "Поздравляю, вы зарегистированы!")
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!")
    bot.send_message(message.chat.id, "Я могу подписать вас на категорию. /sub")
    bot.send_message(message.chat.id, "Я могу отписать вас от категории. /outsub")
    bot.send_message(message.chat.id, "Я могу показать вам новости. /news")

@bot.message_handler(commands=['sub'])
def send_welcome(message):
    bot.send_message(message.chat.id, "На какие категории вы хотели бы подписаться?")
    cats = database.res_sub()
    for item in cats:
        bot.send_message(message.chat.id, f'{item[0]}. {item[1]}')
    mesg = bot.send_message(message.chat.id, 'Выберите категорию (номер):')
    bot.register_next_step_handler(mesg, category_def)

def category_def(message):
    us_id = message.from_user.id
    cat_mes = message.text
    catProvIndef = database.cat_prov_indef(cat_mes)
    if (catProvIndef == None):
        bot.send_message(message.chat.id, 'Такой категории нет.')
    else:
        catProvSub = database.inner_id_cat(us_id, cat_mes)
        if (len(catProvSub) == 0):
            database.sub(us_id, cat_mes)
            bot.send_message(message.chat.id, 'Вы успешно подписались!')
        else:
            bot.send_message(message.chat.id, 'У вас уже есть подписка.')

@bot.message_handler(commands=['outsub'])
def send_welcome(message):
    us_id = message.from_user.id
    bot.send_message(message.chat.id, "От каких категорий вы хотели бы отписаться?")
    cats = database.res_sub_user(us_id)
    for item in cats:
        bot.send_message(message.chat.id, f'{item[0]}. {item[1]}')
    mesg = bot.send_message(message.chat.id, 'Выберите категорию (номер):')
    bot.register_next_step_handler(mesg, category_delete)

def category_delete(message):
    us_id = message.from_user.id
    cat_mes = message.text
    catProvIndefUser = database.cat_prov_indef_user(us_id, cat_mes)
    catProvIndef = database.cat_prov_indef(cat_mes)
    if (catProvIndef == None):
        bot.send_message(message.chat.id, 'Такой категории нет.')
    else:
        if (len(catProvIndefUser) == 0):
            bot.send_message(message.chat.id, 'Вы не подписаны на эту категорию.')
        else:
            database.unsub(us_id, cat_mes)
            bot.send_message(message.chat.id, 'Вы отпиcались от данной категории!')

@bot.message_handler(commands=['news'])
def news_message(message):
    us_id = message.from_user.id
    bot.send_message(message.chat.id, "Какие новости вы хотели бы посмотреть?")
    cats = database.res_sub_user(us_id)
    for item in cats:
        bot.send_message(message.chat.id, f'{item[0]}. {item[1]}')
    mesg = bot.send_message(message.chat.id, 'Выберите категорию (номер):')
    bot.register_next_step_handler(mesg, view_news)

def view_news(message):
    cat_mes = database.name_cat(message.text)[0][0]
    print(cat_mes)
    country = 'ru'
    a = requests.get(f'https://newsapi.org/v2/top-headlines?apiKey={api_key}&category={cat_mes}&pageSize=3&country={country}')
    news = []
    for i in a.json()['articles']:
        news.append([i['title'], i['publishedAt'], i['url']])
    answer = ""
    for line in news:
        answer += converting(line)+"----------------\n"
    bot.send_message(message.chat.id, answer)
    print(news)

@bot.message_handler(content_types=['text'])
def had(message):
    if message.text == 'Как дела?':
        bot.send_message(message.chat.id, "Замурчательно")

bot.infinity_polling()
