from telebot import TeleBot
import telebot
import sys
import os
sys.path.append(os.getcwd())
from logic import TaskManager
bot = TeleBot("8394072241:AAHVZ-52unHvYqeN_-z7ItZdGMZ1Aep_nVc")

task_manager = TaskManager("database.db")
task_manager.create_table()

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-менеджер задач! 
Помогу тебе сохранить твои задачи! 😊

Вот список доступных команд:
/add_task - добавление новой задачи ✏️
/delete_task - удаление задачи 🗑️
/show - показать список задач 📋
/set_deadline - установить дедлайн для задачи ⏰
/clear - удалить все задачи 🧹
/count - подсчитать количество задач 📊
                     
Начнем? Просто выбери команду!""")

@bot.message_handler(commands=['add_task'])
def addtask_command(message):
    bot.send_message(message.chat.id, "Введите название задачи:")
    bot.register_next_step_handler(message, save_task)

def save_task(message):
    name = message.text
    user_id = message.from_user.id 
    task_manager.add_task(user_id, name, '')
    bot.send_message(message.chat.id, "Задача добавлена")

@bot.message_handler(commands=['delete_task'])
def deletetask_command(message):
    bot.send_message(message.from_user.id, "Введите имя задачи, которую хотите удалить:")
    bot.register_next_step_handler(message, delete_task_by_id)

def delete_task_by_id(message):
    user_id = message.from_user.id  
    task_name = message.text
    task_manager.delete_task(task_name, user_id)
    bot.send_message(message.chat.id, "Задача удалена")

@bot.message_handler(commands=['show']) 
def show(message):
    user_id = message.from_user.id 
    arg = telebot.util.extract_arguments(message.text)
    try:
        arg = int(arg)
        tasks = task_manager.show_task_many(user_id, arg)
    except:
        tasks = task_manager.show_task_all(user_id)
    if tasks:
        tasks =  "\n".join([x[0] for x in tasks])
        bot.send_message(message.chat.id, tasks)
    else:
        bot.send_message(message.chat.id, "Задач нет")
        
@bot.message_handler(commands=['set_deadline'])
def set_deadline_command(message):
    bot.send_message(message.chat.id, "Введите название задачи, для которой хотите установить дедлайн:")
    bot.register_next_step_handler(message, ask_deadline)

def ask_deadline(message):
    task_name = message.text
    bot.send_message(message.chat.id, "Введите дедлайн в формате ГГГГ-ММ-ДД:")
    bot.register_next_step_handler(message, lambda msg: save_deadline(msg, task_name))

def save_deadline(message, task_name):
    deadline = message.text
    user_id = message.from_user.id
    if task_manager.set_deadline(user_id, task_name, deadline):
        bot.send_message(message.chat.id, "Дедлайн установлен.")
    else:
        bot.send_message(message.chat.id, "Не удалось найти задачу.")

@bot.message_handler(commands=['clear'])
def clear_command(message):
    user_id = message.from_user.id
    task_manager.clear_all(user_id)
    bot.send_message(message.chat.id, "Все задачи удалены 🧹")

@bot.message_handler(commands=['count'])
def count_command(message):
    user_id = message.from_user.id
    count = task_manager.count_tasks(user_id)
    bot.send_message(message.chat.id, f"У тебя {count} задач(и) 📋")


bot.infinity_polling()
