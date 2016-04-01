# coding: utf-8

#######################################
# Telegram logging bot.
# Author: Artyom Chizhov (@artchizhov) artchizhov@gmail.com
# (Based at Talisman / Isida)
# Dependencies: telepot
# SETTINGS: write you token at bottom of file ...
#######################################

import telepot

import os
import time
import threading


BOT_PREFIX = '/'
PLUGINS_DIR = 'plugins/'


commands = []
message_handlers = []


mtx = threading.Lock()


def read_file(filename):
    fp = file(filename, 'r')
    data = fp.read()
    fp.close()
    return data


def write_file(filename, data):
    mtx.acquire()
    fp = file(filename, 'w')
    fp.write(data)
    fp.close()
    mtx.release()


def error(text):
    print "ERROR: " + text


def warning(text):
    print "WARNING: " + text


def command_default(data):
    chat = data['chat']
    text = data['text']

    bot.sendMessage(chat['id'], 'Command ' + text + ' not found.\nType ' + BOT_PREFIX + 'help')


def message(data):
    text = data['text']
    if text[0] == BOT_PREFIX:
        for comm in commands:
            if text == BOT_PREFIX + comm['tag']:
                print 'Got command: ' + BOT_PREFIX + comm['tag']
                comm['func'](data)
                break
            #else:  FIXME
            #    warning('Command ' + text + ' not found.')
            #    command_default(data)
    else:
        for msg_hdlr in message_handlers:
            msg_hdlr(data)


plugins_folder = 'plugins/%s'
plugins_file_list = os.listdir(plugins_folder % '')

for plugin_file in plugins_file_list:
    if plugin_file.endswith('.py'):
        print('loading '+plugin_file+'...')
        execfile(plugins_folder % plugin_file)

bot = telepot.Bot('token')
bot.notifyOnMessage(message)

print 'Bot started. Listening ...'
while True:
    time.sleep(10)