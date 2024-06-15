import telebot  # Импортируем библиотеку telebot для работы с Telegram API
import wikipedia  # Импортируем библиотеку wikipedia для работы с Википедией
from logic import DBManager

manager = DBManager


API_TOKEN = '6730463524:AAGIzrWjKdZf97arCExMn98EMC8GMKsI2pI'  # Замените 'api' на ваш реальный API токен
bot = telebot.TeleBot(API_TOKEN)  # Создаем объект бота

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Это бот для поиска информации. Обратитесь к команде /help, если вы здесь впервые.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Список команд:\n/search - поиск\n/login - для изменения своего аккаунта")

# Обработчик команды /search
@bot.message_handler(commands=['search'])
def search(message):
    lang = "ru"  # Получение языка из базы данных
    wikipedia.set_lang(lang)  # Устанавливаем язык для Wikipedia API
    bot.reply_to(message, "Введите информацию для поиска")
    bot.register_next_step_handler(message, search_step_2)  # Переходим к следующему шагу поиска

# Следующий шаг поиска
def search_step_2(message):
    user_input = message.text  # Получаем текст сообщения от пользователя
    article = wikipedia.search(user_input)  # Ищем статьи в Википедии по введенному запросу
    for i in article:
        bot.reply_to(message, i)  # Отправляем список найденных статей
    bot.reply_to(message, "Скопируйте название статьи из списка или напишите что-то другое")
    bot.register_next_step_handler(message, process_article)  # Переходим к следующему шагу обработки статьи

# Обработка выбранной статьи
def process_article(message):
    try:
        len_mes = "1"  # Получение предпочтений по длине статьи (1 - полная, 2 - краткая)
        user_input = message.text  # Получаем текст сообщения от пользователя
        if len_mes == "1":
            article = wikipedia.page(user_input)  # Получаем полную статью
            bot.reply_to(message, article.content)  # Отправляем содержимое статьи пользователю
        elif len_mes == "2":
            article = wikipedia.summary(user_input)  # Получаем краткое содержание статьи
            bot.reply_to(message, article.content)  # Отправляем краткое содержание пользователю
    except Exception as e:  # Обработка исключений
        bot.reply_to(message, "Не удалось найти статью")  # Сообщаем пользователю об ошибке

# Обработчик команды /login
@bot.message_handler(commands=["login"])
def log(message):
    bot.reply_to(message, 'Для улучшения качества сервиса мы зададим вам несколько вопросов.')
    all_lang = wikipedia.languages()  # Получаем список доступных языков
    bot.reply_to(message, "Введите язык")
    bot.register_next_step_handler(message, process_lang, all_lang)  # Переходим к следующему шагу обработки языка

# Обработка введенного языка
def process_lang(message, all_lang):
    user_lang = message.text  # Получаем текст сообщения от пользователя
    if user_lang not in all_lang:  # Проверяем, существует ли введенный язык
        bot.reply_to(message, "Вашего языка нет в списке")
        bot.register_next_step_handler(message, process_lang, all_lang)
    else:
        bot.reply_to(message, "Идем дальше.")
        bot.reply_to(message, "На сколько длинной будет статья: 1 - полная или 2 - краткая? Введите номер.")
        bot.register_next_step_handler(message, process_len, user_lang)  # Переходим к следующему шагу обработки длины статьи

# Обработка введенной длины статьи
def process_len(message, user_lang):
    user_len = message.text
    user_id = message.from_user.id
    if user_len in ["1", "2"]:
        manager.save_user_preferences(user_id, user_lang, user_len)
        bot.reply_to(message, "Настройки сохранены.")
    else:
        bot.reply_to(message, "Ошибка. Попробуйте еще раз.")
        bot.register_next_step_handler(message, process_len, user_lang)

bot.infinity_polling()  # Запуск бесконечного цикла для обработки сообщений
