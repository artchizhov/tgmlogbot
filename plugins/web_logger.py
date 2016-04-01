# coding: utf-8

import os
import time


WEB_LOGGER_DIR = PLUGINS_DIR + 'web_logger.dir/'
WEB_LOGGER_TEMPLATE = WEB_LOGGER_DIR + 'template.html'


def web_logger_save(chat, ldate, ltime, logline):
    (year, month, day) = ldate

    str_year = '%.4i' % year
    str_month = '%.2i' % month
    str_day = '%.2i' % day

    str_date = '%s/%s/%s' % (str_day, str_month, str_year)

    logpath = WEB_LOGGER_DIR + '%s/%s/%s/' % (chat, str_year, str_month)
    logfile = logpath + '%s.html' % str_day
    if not os.path.exists(logfile):
        try:
            os.makedirs('/'.join(['plugins', 'web_logger.dir', chat, str_year, str_month]))  # FIXME
        except:
            pass  # FIXME

        template = read_file(WEB_LOGGER_TEMPLATE)

        template = template.replace('<!--[title]-->', chat).replace('<!--[room]-->', chat).replace('<!--[date]-->', str_date)
        template = template.replace('<!--[log_line]-->', logline)

        write_file(logfile, template.encode('utf-8'))
    elif os.path.exists(logfile):
        write_file(logfile, read_file(logfile).replace('<!--[log_line]-->', logline.encode('utf-8')))
    else:
        error('[WEB_LOGGER] - Could not write log')


def web_logger(data):
    text = data['text']

    if not text:
        return

    # FIXME
    title = None
    username = None
    first_name = None
    last_name = None

    try:
        room = data['chat']
        title = room['title']
    except KeyError:
        error('[WEB_LOGGER] - KeyError (room)')

    try:
        sender = data['from']
        username = sender['username']
        first_name = sender['first_name']
        last_name = sender['last_name']
    except KeyError:
        error('[WEB_LOGGER] - KeyError (sender)')

    ldate = time.localtime()[:3]
    ltime = time.localtime()[3:-3]

    text = text.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('\n', '<br />')

    full_name = '@%s [%s %s]' % (username, first_name, last_name)
    tstamp = '%.2i:%.2i:%.2i' % ltime

    logline = '<p class="logline">'
    logline = logline + '<span class="tstamp"><a id="t' + tstamp + '" href="#t' + tstamp + '">' + tstamp + '</a></span>'
    logline = logline + ' <span class="name">' + full_name + '</span>'
    logline = logline + ': <span class="text">' + text + '</span>'
    logline = logline + '</p>'
    logline = logline + '\n<!--[log_line]-->'

    if title is not None:
        chat = title
    elif username is not None:
        chat = username
    else:
        chat = 'unnamed'  # FIXME

    web_logger_save(chat, ldate, ltime, logline)


message_handlers.append(web_logger)