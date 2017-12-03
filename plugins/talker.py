# coding: utf-8

import time
import random
import datetime


TALKER_DIR = '%stalker.dir/' % settings['plugins_dir']
ANSWERS_FILE = '%sanswer_db.txt' % TALKER_DIR

ansfp = file(ANSWERS_FILE, 'r')
answers = ansfp.readlines()
anscount = len(answers)
ansfp.close()


def talker(data):
    chat = data['chat']
    sender = data['from']
    username = sender.get('username', '')
    
    text = data.get('text', '')
    
    if (text.find(settings['nick']) is not -1) or (text.find(settings['username']) is not -1):
        bot.sendMessage(chat['id'], '@%s: %s' % (username, answers[random.randint(0, anscount-1)].decode('UTF-8')))
    elif random.randint(0,10) == 6:
        bot.sendMessage(chat['id'], answers[random.randint(0, anscount-1)].decode('UTF-8'))


def talk(data):
    chat = data['chat']
    sender = data['from']
    username = sender.get('username', '')
    
    text = data.get('text', '')
    
    bot.sendMessage(chat['id'], answers[random.randint(0, anscount-1)].decode('UTF-8'))


commands.append(('talk', talk))
message_handlers.append(talker)