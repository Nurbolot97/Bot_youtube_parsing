from selenium import webdriver
from decouple import config
import telebot
from telebot import types
from time import sleep

driver = webdriver.Firefox()
bot = telebot.TeleBot(config('TOKEN'))

@bot.message_handler(commands=['start', 'старт'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Приветсвую Вас! Для дальнейших действий можете набрать команды")

@bot.message_handler(commands=['search_clip'])
def search_clip(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Для поиска видеоклипа напишите название пожалуйста!")
    bot.register_next_step_handler(msg, search_clip_video)

def search_clip_video(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Начинаю поиск, ожидайте...")
    clip_href = 'https://www.youtube.com/results?search_query=' + message.text
    driver.get(clip_href)
    sleep(2)
    clips = driver.find_elements_by_id('video-title')
    bot.send_message(chat_id, "Результаты поиска:")
    for i in range(len(clips)):
        bot.send_message(chat_id, f"{clips[i].get_attribute('href')}")
        if i == 10:
            break
      
@bot.message_handler(commands=['search_clip_channel'])
def search_channel(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Для поиска канала вставьте URL-адрес!")
    bot.register_next_step_handler(msg, search_clip_channel)

def search_clip_channel(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Начинаю поиск, ожидайте...")
    if (message.text).startswith('https://www.youtube.com'):
        driver.get(message.text + '/videos')
        clips = driver.find_elements_by_id('video-title')
        bot.send_message(chat_id, "Результаты поиска:")
        for i in range(len(clips)):
            bot.send_message(chat_id, f"{clips[i].get_attribute('href')}")
            if i == 10:
                break
    else:
        bot.send_message(chat_id, 'URL is invalid')

def main():
    bot.polling()

if __name__ == "__main__":
    main()















































