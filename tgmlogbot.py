# coding: utf-8

#######################################
# Telegram logging bot.
# Author: Artyom Chizhov (@artchizhov) artchizhov@gmail.com
# (Based at Talisman / Isida)
# Dependencies: telepot
#######################################

import os
import time
import sys
import threading

sys.path = ['./lib'] + sys.path

import telepot


config = 'settings.py'

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
    print "ERROR: %s" % text


def warning(text):
    print "WARNING: %s" % text


def command_default(data):
    chat = data['chat']
    text = data['text']

    bot.sendMessage(chat['id'], 'Command %s not found.\nType %shelp' % (text, settings['command_prefix']))


def message(data):
    text = data.get('text', '')
    
    if text is not '':
        if text[0] == settings['command_prefix']:
            
            # FIXME optimize
            text = text.replace('@%s' % settings['username'], '') # remove @UserName from /command@UserName args
            textspl = text.split(' ', 1)
            raw_comm = textspl[0]
            if len(textspl) > 1:
                raw_arg = textspl[1]
            else:
                raw_arg = ''
            
            for comm in commands:
                if raw_comm == settings['command_prefix'] + comm[0]:
                    print 'Got command: %s%s' % (settings['command_prefix'], comm[0])
                    data['text'] = raw_arg
                    comm[1](data)
                    break
                #else:  FIXME
                #    warning('Command ' + text + ' not found.')
                #    command_default(data)
        else:
            for msg_hdlr in message_handlers:
               msg_hdlr(data)


if __name__ == "__main__":
    if os.path.isfile(config):
        execfile(config)

        plugins_file_list = os.listdir(settings['plugins_dir'])

        for plugin_file in plugins_file_list:
            if plugin_file.endswith('.py'):
                print('Loading %s...' % plugin_file)
                execfile(settings['plugins_dir'] + plugin_file)

        bot = telepot.Bot(settings['token'])
        bot.notifyOnMessage(message)

        print '\nBot started. Listening ...'
        while True:
            time.sleep(10)
    else:
        error('Config file "%s" not found!\nExiting...' % config)