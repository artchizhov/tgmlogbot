# coding: utf-8

import time
import random
import datetime


def main_help(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "I can not help you now... :(")
    pass


def main_say(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "I say.")
    pass


def main_time(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "May be later, ok?")
    pass


def main_date(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "May be later, ok?")
    pass


def main_google(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "I love Google!")
    pass


def main_bash(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], "I tired, later please.")
    pass


def main_roll(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    bot.sendMessage(chat['id'], random.randint(1,6))
    pass


def main_test(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    #bot.sendMessage(chat['id'], 'Passed')

    (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()

    str_time = str(year)+'-'+str(month)+'-'+str(day)+' '+str(hour)+':'+str(minute)+':'+str(second)

    bot.sendMessage(chat['id'], 'USER: '+sender['first_name']+' '+sender['last_name']+' SEND MESSAGE: '+text+' IN CHAT: '+chat['title']+' AT LOCAL TIME: '+str_time)
    pass


commands.append({'tag': 'help',     'func': main_help})
commands.append({'tag': 'say',      'func': main_say})
commands.append({'tag': 'time',     'func': main_time})
commands.append({'tag': 'date',     'func': main_date})
commands.append({'tag': 'google',   'func': main_google})
commands.append({'tag': 'bash',     'func': main_bash})
commands.append({'tag': 'roll',     'func': main_roll})
commands.append({'tag': 'test',     'func': main_test})

#message_handlers.append(test_msg)