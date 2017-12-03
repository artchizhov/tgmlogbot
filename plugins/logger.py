# coding: utf-8

import os
import time
import re


LOGGER_DIR = '%slogger.dir/' % settings['plugins_dir']


# You can change default Logs path here:
LOGS = LOGGER_DIR  # + 'logs/'

# You can change default template path here:
LOGGER_TEMPLATE = '%s_template/template.html' % LOGGER_DIR


def logger_save(chat, ldate, logline):
    sYear = '%.4i' % ldate[0]
    sMonth = '%.2i' % ldate[1]
    sDay = '%.2i' % ldate[2]

    sDate = '%s/%s/%s' % (sDay, sMonth, sYear)

    logpath = '%s%s/%s/%s/' % (LOGS, chat, sYear, sMonth)
    logfile = '%s%s.html' % (logpath, sDay)

    if not os.path.exists(logfile):
        try:
            os.makedirs(logpath)
        except:
            error('[LOGGER] - Could not create log file ("%s").' % logfile)

        template = read_file(LOGGER_TEMPLATE)

        template = template.replace('<!--[title]-->', chat).replace('<!--[room]-->', chat).replace('<!--[date]-->', sDate)
        template = template.replace('<!--[log_line]-->', logline)

        write_file(logfile, template.encode('utf-8'))
    elif os.path.isfile(logfile):
        write_file(logfile, read_file(logfile).replace('<!--[log_line]-->', logline.encode('utf-8')))
    else:
        error('[LOGGER] - Could not write log ("%s").' % logfile)


def logger(data):
    room = data['chat']
    sender = data['from']
    text = data['text']

    title = room.get('title', '')
    username = sender.get('username', '')
    first_name = sender.get('first_name', '')
    last_name = sender.get('last_name', '')

    ldate = time.localtime()[:3]
    ltime = time.localtime()[3:-3]

    text = text.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br />')

    full_name = '@%s [%s %s]' % (username, first_name, last_name)
    tstamp = '%.2i:%.2i:%.2i' % ltime

    logline = '<p class="logline">'
    logline = logline + '<span class="tstamp"><a id="t%s" href="#t%s">%s</a></span>' % (tstamp, tstamp, tstamp)
    logline = logline + ' <span class="name">%s</span>' % full_name
    logline = logline + ': <span class="text">%s</span>' % text
    logline = logline + '</p>'
    logline = logline + '\n<!--[log_line]-->'
    
    simple_reg = re.compile('[^0-9a-zA-Zа-яА-Я _]')
    title_simple = simple_reg.sub('', title)
    username_simple = simple_reg.sub('', username)

    if title_simple is not '':
        chat = title_simple
    elif username_simple is not '':
        chat = username_simple
    else:
        chat = 'unnamed'

    logger_save(chat, ldate, logline)


message_handlers.append(logger)
