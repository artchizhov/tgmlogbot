# coding: utf-8

import random


def true(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']
    
    if text is not '':
        bot.sendMessage(chat['id'], u'Вероятность того, что %s - %i%%' % (text, random.randint(0, 100)))
    else:
        bot.sendMessage(chat['id'], u'И чё?')


commands.append(('true', true))

#message_handlers.append(test_msg)