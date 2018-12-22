import collections
import fileinput
import mailbox
import string
from stop_words import get_stop_words
import html
import json
from html.parser import HTMLParser
import operator
import re

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def remove_punc(u):
	for s in string.punctuation:
  		u = u.replace(s,'')
	return u

def rerere(message):
	bb = ''
	for part in message.get_payload():
			if not part.is_multipart():
				bb += part.get_payload()
			else:
				bb += rerere(part)
	return bb

def clean(txt):
	l = txt.split(' ')
	ll = l[-1].split('<')
	return ll[-1].strip('>')


def run(filepath,ddd):
    list_wc = []
    list_etc = []
    list_wc_edge = []
    edges_undi = []

    mapp_list = []

    stop_words = get_stop_words('en')
    worddict = {}
    list_wc = []
    list_content = []


    for message in mailbox.mbox(filepath):

    	mapp = {}
    	c_from = clean(message['From'])
    	c_to = clean(message['To'])
    	subject = message['subject']
    	date = message['date']

    	list_etc.append([c_from,c_to,subject,date])

    	edge_undi = set()
    	edge_undi.update([c_from,c_to])

    	buf = {}


    	if message.is_multipart():
    		b =''
    		b += rerere(message)
    		list_content.append(b)
    		b = html.unescape(b)
    		b = strip_tags(b)
    		buf = collections.Counter([w for w in remove_punc(b).lower().split() if not (w in stop_words) and (bool(re.match(r"^[a-zA-Z]+$",w))) and not (bool(re.match(r"^[0-9]+$", w)))])
    		list_wc.append(buf)

    	else:
    		list_content.append(message.get_payload())
    		buf = collections.Counter([w for w in remove_punc(message.get_payload()).lower().split() if not (w in stop_words) and (bool(re.match(r"^[a-zA-Z]+$",w))) and not (bool(re.match(r"^[0-9]+$", w)))])
    		list_wc.append(buf)


    	if edge_undi not in edges_undi:
    		mapp['con'] = edge_undi
    		mapp['wc'] = buf
    		mapp_list.append(mapp)
    		edges_undi.append(edge_undi)
    	else:
    		for i in mapp_list:
    			if i['con'] == edge_undi:
    				l_tmp = []
    				l_tmp.append(i['wc'])
    				l_tmp.append(buf)
    				i['wc'] = sum((collections.Counter(dict(x)) for x in l_tmp),collections.Counter())

    ac = sum((collections.Counter(dict(x)) for x in list_wc),collections.Counter())


    all_wc = []
    all_wcc = {}
    all_wc_count = len(ac)



    for i in sorted(ac,key=ac.get,reverse=True)[:60]:
    	all_wcc[i] = ac[i]


    mapp_list_fin = []
    edge_wc_count_list = []


    for i in mapp_list:
    	mapp_list_fin.append(i['wc'])

    for i in mapp_list_fin:
        edge_wc_count_list.append(len(i))
        tm = {}
        for q in sorted(i,key=i.get,reverse=True)[:60]:
            tm[q] = i[q]
        i = tm

    all_wc.append(all_wcc)

    ddd['all_wc_60'] = all_wc
    ddd['list_content'] = list_content
    ddd['list_con_etc'] = list_etc
    ddd['all_wc_count'] = all_wc_count
    ddd['list_wc'] = list_wc
    ddd['edge_wc_60'] = mapp_list_fin
    ddd['edge_wc_count_list'] = edge_wc_count_list
    return ddd


#jsonfile = open('wc3.json', 'w')
# j = open('content.json','w')
# j2 = open('con_etc.json','w')
#j3 = open('all_wc_80.json','w')
#j4 = open('all_wc_count.json','w')
#j5 = open('edge_wc_top80.json','w')
#json.dump(all_wc,j3)
# json.dump(list_etc,j2)
# json.dump(list_content,j)
#json.dump(list_wc,jsonfile)
#json.dump(all_wc_count,j4)
#json.dump(mapp_list_fin,j5)
