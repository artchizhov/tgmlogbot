# coding: utf-8

import urllib2
import re


def bash(data):
    chat = data['chat']
    sender = data['from']
    text = data['text']

    text = text.strip()
    if not text:
        url = 'http://bash.im/random'
    elif re.match('\d+$', text):
        url = 'http://bash.im/quote/%s' % text
    else:
        pass
        #url = 'http://bash.im/?text=%s' % urllib.quote(text.encode('cp1251'))

    #body = html_encode(load_page(url))
    #body = re.findall('<span class="date">(.*?)</span>.*?class="id">(.*?)</a>.*?<div class="text">(.*?)</div>', body, re.S|re.I|re.U)

    #body = urllib.urlopen('http://bash.im/random').read().decode("utf-8")

    req = urllib2.Request('http://bash.im/forweb/?u', headers={'User-Agent': 'Mozilla/5.0'})
    body = urllib2.urlopen(req).read().decode("utf-8")
    body = re.sub("' *\+ *'", '', body)

    ''.join(xml.etree.ElementTree.fromstring(text).itertext())

    body = re.findall('b_q_t.*</div>', body)[0]
    body = re.sub('<br[^>]*>', '\n', body)
    body = re.sub('<div[^>]*>', '', body)
    body = re.sub('</div>', '\n', body)

    #bot.sendMessage(chat['id'], body)
    print body


def ibash(data):
	pass
#	reg_title = '<div class="quothead">.*?<b>#(.*?)</b>'
#	reg_body = '<div class="quotbody">(.*?)</div>'
#	url_id = 'http://ibash.org.ru/quote.php?id='
#	try: url = url_id+str(int(text))
#	except: url = 'http://ibash.org.ru/random.php'
#	body = html_encode(load_page(url))
#	msg = url_id + re.findall(reg_title, body, re.S)[0]
#	if msg[-3:] == '???': msg = L('Quote not found!','%s/%s'%(jid,nick))
#	else: msg += '\n'+rss_replace(re.findall(reg_body, body, re.S)[0])
#	send_msg(type, jid, nick, msg)


commands.append(('bash', bash))
commands.append(('ibash', ibash))