import mailbox
import json
import random
#jsonfile = open('recgraph.json', 'w')
def run(filepath):
	qw = 0
	data = []
	for message in mailbox.mbox(filepath):
		#print("iter" + str(qw))
		qw += 1
		nodeRs = []
		edgeRs = []
		tmplist = []
		nodeR_size = {}
		received_list = []
		for i in message.items():
			if i[0] == 'Received':
				received_list.append(i[1])
		for i in received_list:
			edgeR = {}
			by = i.split('by')[1].split(' ')[1]
			fromm = i.split(' ')[1]

			if by not in tmplist:
				tmplist.append(by)
				nodeR_size[by] = 10
			if fromm not in tmplist:
				tmplist.append(fromm)
				nodeR_size[fromm] = 10

			edgeR['by'] = by
			edgeR['fromm'] = fromm
			if edgeR not in edgeRs:
				edgeRs.append(edgeR)
		ttt = 0
		for i in tmplist:
			color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
			nodeR = {}
			nodeR['id'] = i
			nodeR['x'] = 50 + ttt
			nodeR['y'] = 50
			nodeR['size'] = nodeR_size[i]
			nodeR['attributes'] = {}
			nodeR['label'] = i
			nodeR['color'] = color
			nodeRs.append(nodeR)
			ttt += 50

		dataa = {}
		dataa['nodes'] = nodeRs
		dataa['edges'] = edgeRs
		data.append(dataa)
	return data


#json.dump(data, jsonfile)
