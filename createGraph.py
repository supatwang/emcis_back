import mailbox
import random
import json
from collections import defaultdict


def clean(txt):
	l = txt.split(' ')
	ll = l[-1].split('<')
	return ll[-1].strip('>')

def eee(mlist):
	for i in mlist:
		i = i.split('by').split(' ')

def run(filename):
	nodes = []
	node_size = {}
	edges = []
	edges_undi = []
	temp = {}
	#jsonfile = open('mail3.json', 'w')
	message_id = 0
	edge_id = 0
	node_num = 0

	for message in mailbox.mbox(filename):
		edge_undi = set()
		edge = defaultdict(list)
		c_from = clean(message['From'])
		c_to = clean(message['To'])

		if c_from not in temp:
			temp[c_from] = c_from
			node_size[c_from] = 10

		else:
			node_size[c_from] += 1

		if c_to not in temp:
			temp[c_to] = c_to
			node_size[c_to] = 10

		edge['From'] = c_from
		edge['To'] = c_to

		edge_undi.update([c_from,c_to])

		if edge_undi not in edges_undi:
			edge['message_list'].append(message_id)
			edge['message_count'] = 1
			edge['id'] = edge_id
			edge_id += 1
			edges.append(edge)
			edges_undi.append(edge_undi)
		else:
			for i in edges:
				if i['From'] == c_from and i['To'] == c_to:
					i['message_list'].append(message_id)
					i['message_count'] += 1
					break
				if i['From'] == c_to and i['To'] == c_from:
					i['message_list'].append(message_id)
					i['message_count'] += 1
					break

		message_id += 1


	for i in temp:
		color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
		node = {}
		node['id'] = i
		node['x'] = random.uniform(-1000, 1000)
		node['y'] = random.uniform(-1000, 1000)
		if node_size[i] > 20:
			node['size'] = int(20 + node_size[i]/20)	
		else:
			node['size'] = node_size[i]
		node['sent_count'] = node_size[i] - 9
		node['attributes'] = {}
		node['label'] = i
		node['color'] = color
		nodes.append(node)
		node_num += 1

	data = {}
	data['nodes'] = nodes
	data['edges'] = edges
	data['count_all_mail'] = message_id
	data['count_all_edge'] = edge_id
	data['count_all_node'] = node_num
	return data
	
#print(edges_undi)

#json.dump(data, jsonfile)
