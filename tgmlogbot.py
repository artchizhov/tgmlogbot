# -*- coding: utf-8 -*-

#######################################
# Bot for Telegram
# Author: Artyom Chizhov @artchizhov (artchizhov@gmail.com)
# 2016
# (Based at Telepot and XMPP TalismanBot)
# SETTINGS: write you token at bottom of file ...
#######################################

import telepot

import os
import re
import sys
import time
import math
import random
import datetime
import threading


mtx = threading.Lock()

def read_file(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def write_file(filename, data):
	mtx.acquire()
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()
	mtx.release()


LOGDIR			= 'log/'
LOG_CACHE_FILE		= 'log/cache.txt'
LOG_FILENAME_CACHE	= eval(read_file(LOG_CACHE_FILE))

BOTPREFIX	= '/'


###### Commands [ ######
def comm_help(chat, user, command):
        bot.sendMessage(chat['id'], "I can not help you now... :(")
        pass
        
def comm_say(chat, user, command):
        bot.sendMessage(chat['id'], "I say.")
        pass

def comm_time(chat, user, command):
        bot.sendMessage(chat['id'], "May be later, ok?")
        pass

def comm_date(chat, user, command):
        bot.sendMessage(chat['id'], "May be later, ok?")
        pass

def comm_google(chat, user, command):
        bot.sendMessage(chat['id'], "I love Google!")
        pass

def comm_bash(chat, user, command):
        bot.sendMessage(chat['id'], "I tired, later please.")
        pass

def comm_roll(chat, user, command):
        bot.sendMessage(chat['id'], random.randint(1,6))
        pass

def comm_test(chat, user, command):
        #bot.sendMessage(chat['id'], 'Passed')

	(year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()

	str_time = str(year)+'-'+str(month)+'-'+str(day)+' '+str(hour)+':'+str(minute)+':'+str(second)

	bot.sendMessage(chat['id'], 'USER: '+user['first_name']+' '+user['last_name']+' SEND MESSAGE: '+command+' IN CHAT: '+chat['title']+' AT LOCAL TIME: '+str_time)

        pass
###### ] Commands ######


###### Logging [ ######
def log_write_header(fp, chat_name, (year, month, day, hour, minute, second)):
	str_time = str(year)+'-'+str(month)+'-'+str(day)+' '+str(hour)+':'+str(minute)+':'+str(second)
	fp.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>%s</title>
<style type="text/css">
body {font-family:"Segoe UI";font-size:11pt;margin:0pt;padding: 6pt 10pt 6pt 10pt;background-color:#eee;
/* background-image:url(i/back2.gif) */background-image:url(bg.gif);}
.wrapper, .content {border-color:#222;}
.wrapper {border-style:solid;border-width:1pt;background-color:#FFF;}
.header {background-color:#222;padding: 1pt 4pt 2pt 4pt;}
a.room, .date {color: #ddd;}
a.room {text-decoration:none;font-weight:bold;}
a.room:hover {color:#39F;}
.content {border-top-style:solid;border-top-width:1pt;padding: 2pt 4pt 0pt 4pt;}
p.logline {margin:0pt 0pt 2pt 0pt;border-style:solid;border-width:1pt;border-color:#ddd;background-color:#eee;padding:1pt 2pt 1pt 2pt;}
.tstamp a {text-decoration:none;color:#036;}
.tstamp a:hover {color:#630;}
.name {font-weight:bold;color:#060;}
</style>
</head>
<body>
<div class="wrapper">
<div class="header">
<a class="room" href="https://example.com" title="Join">%s</a>
<span class="date"> - %s</span>
</div>
<div class="content">
""" % (' - '.join([chat_name, str_time]), chat_name, chat_name, str_time))
	pass

def log_write_footer(fp):
	fp.write("""</div>
</div>
</body>
</html>
""")
	pass

def log_get_fp(chat_name, (year, month, day, hour, minute, second)):
	str_year = str(year)
	str_month = str(month)
	str_day = str(day)
	
	filename = '.'.join(['/'.join([LOGDIR, chat_name, str_year, str_month, str_day]), 'html'])
	alt_filename = '.'.join(['/'.join([LOGDIR, chat_name, str_year, str_month, str_day]), '_alt.html'])
	if not os.path.exists('/'.join([LOGDIR, chat_name, str_year, str_month])):
		os.makedirs('/'.join([LOGDIR, chat_name, str_year, str_month]))
	
	if LOG_FILENAME_CACHE.has_key(chat_name):
		if LOG_FILENAME_CACHE[chat_name] != filename:
			fp_old = file(LOG_FILENAME_CACHE[chat_name], 'a')
			log_write_footer(fp_old)
			fp_old.close()
		if os.path.exists(filename):
			fp = file(filename, 'a')
			return fp
		else:
			LOG_FILENAME_CACHE[chat_name] = filename
			write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
			fp = file(filename, 'w')
			log_write_header(fp, chat_name, (year, month, day, hour, minute, second))
			return fp
	else:
		if os.path.exists(filename):
			LOG_FILENAME_CACHE[chat_name] = filename
			write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
			fp = file(alt_filename, 'a')
			return fp
		else:
			LOG_FILENAME_CACHE[chat_name] = filename
			fp = file(filename, 'w')
			log_write_header(fp, chat_name, (year, month, day, hour, minute, second))
			return fp
	pass

def log_regex_url(matchobj):
	return '<a href="' + matchobj.group(0) + '">' + matchobj.group(0) + '</a>'
	pass

def log(chat, user, text):
	if not text: return

	chat_title      = ''
        username        = ''
        first_name      = ''
        last_name       = ''

	try:
		chat_title      = chat['title']
        	username        = user['username']
        	first_name      = user['first_name']
        	last_name       = user['last_name']
	except:
		pass

	chat_name = chat_title
	user_name = '@'+username+' ('+first_name+' '+last_name+')'
	
	decimal = str(int(math.modf(time.time())[0]*100000))
	(year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
	
	text = text.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
	text = re.sub('(http|ftp)(\:\/\/[^\s<]+)', log_regex_url, text)
	text = text.replace('\n', '<br/>')
	text = text.encode('utf-8');
	user_name = user_name.encode('utf-8');
	
	timestamp = '[%.2i:%.2i:%.2i]' % (hour, minute, second)
	
	fp = log_get_fp(chat_name, (year, month, day, hour, minute, second))
	fp.write('<p class="logline">')
	fp.write('<span class="tstamp"><a id="t' + timestamp[1:-1] + '.' + decimal + '" href="#t' + timestamp[1:-1] + '.' + decimal + '">' + timestamp + '</a></span>')
	fp.write('<span class="name">&lt;%s&gt;</span><span class="text">%s</span>\n' % (user_name, text))
	fp.write('</p>')
	fp.close()

	pass
###### ] Logging ######

def handle_message(msg):
	chat	= msg['chat']
	user	= msg['from']
	text	= msg['text']

	if text[0] == BOTPREFIX:
		command = text
	
		print 'Got command: %s' % command

		if	command == '/help':	comm_help(chat, user, command)
		elif	command == '/say':	comm_say(chat, user, command)
		elif	command == '/time':	comm_time(chat, user, command)
		elif	command == '/date':	comm_date(chat, user, command)
		elif	command == '/google':	comm_google(chat, user, command)
		elif	command == '/bash':	comm_bash(chat, user, command)
		elif	command == '/roll':	comm_roll(chat, user, command)
		elif	command == '/test':	comm_test(chat, user, command)
	
	log(chat, user, text)
	pass


bot = telepot.Bot('<<token>>')

bot.notifyOnMessage(handle_message)

print 'I am listening ...'

while 1:
	time.sleep(10)