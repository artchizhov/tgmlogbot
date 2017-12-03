# coding: utf-8

import time
import random
import datetime


def main_help(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "I can not help you now... :(")


def main_say(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "I say.")


def main_time(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "May be later, ok?")


def main_date(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "May be later, ok?")


def main_google(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "I love Google!")


def main_roll(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']
    
    username = sender.get('username', '')
    first_name = sender.get('first_name', '')
    last_name = sender.get('last_name', '')
    
    a = random.randint(1,4)
    b = random.randint(1,4)
    
    if a == b:
        bot.sendMessage(chat['id'], '%s %s %s' % (first_name, last_name, u'Вы убиты!'))
    else: # FIXME optimize
        if random.randint(1,3) == 3:
            bot.sendMessage(chat['id'], u'Продолжай смотреть на лампочку.')
        else:
            bot.sendMessage(chat['id'], u'Крути дальше...')


def main_test(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], 'Passed!')


commands.append(('help', main_help))
commands.append(('say', main_say))
commands.append(('time', main_time))
commands.append(('date', main_date))
commands.append(('google', main_google))
commands.append(('roll', main_roll))
commands.append(('test', main_test))

#message_handlers.append(test_msg)