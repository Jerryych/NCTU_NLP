import pysrt
from opencc import OpenCC
from pycorenlp import StanfordCoreNLP
import json
import math


occ1 = OpenCC('t2s')
subs = pysrt.open('./traditional/You Are the Apple of My Eye.srt')
with open('./simplified/You Are the Apple of My Eye.txt', 'w') as f:
	print('T to S: You Are the Apple of My Eye')
	for sub in subs:
		subSimplified = occ1.convert(sub.text)
		f.write(subSimplified + '\n')
	print('Save to ./simplified/You Are the Apple of My Eye.txt')

nlp = StanfordCoreNLP('http://localhost:9000')

segments = []
occ2 = OpenCC('s2t')
print('Read ./simplified/You Are the Apple of My Eye.txt')
with open('./simplified/You Are the Apple of My Eye.txt', 'r') as movielines:
	for movieline in movielines:
		output = nlp.annotate(movieline.rstrip(), properties={'annotators': 'pos', 'pipelineLanguage': 'zh', 'outputFormat': 'json'})
		sentences = output['sentences']
		for sentence in sentences:
			tokens = sentence['tokens']
			for token in tokens:
				token['word'] = occ2.convert(token['word'])
			segments.append(tokens)

with open('./parsing_result/You Are the Apple of My Eye.json', 'w') as jsonFile:
	json.dump(segments, jsonFile)
	print('Save to ./parsing_result/You Are the Apple of My Eye.json')

with open('./parsing_result/You Are the Apple of My Eye.json', 'r') as jsonFile:
	lines = json.load(jsonFile)

xtargets = ['喜歡', '打', '追']
pxtargets = ['VV', 'VV', 'VV']
pytargets = ['NN', 'NN', 'PN']
ytargets = ['妳', '手槍', '她']
xset = {'喜歡':0, '打': 1, '追':2}
yset = {'妳': 0, '手槍': 1, '她': 2}
xCnt = [0, 0, 0]
yCnt = [0, 0, 0]
xyCnt = [0, 0, 0]
xExist = False
yExist = False
colloc = False
for line in lines:
	for token in line:
		if token['word'] in xtargets and not xExist:
			if token['pos'] == pxtargets[xset[token['word']]]:
				xCnt[xset[token['word']]] += 1
				xExist = True
		elif token['word'] in ytargets and not yExist:
			if token['pos'] == pytargets[yset[token['word']]]:
				yCnt[yset[token['word']]] += 1
				yExist = True
		if xExist and yExist and not colloc:
			if token['word'] in xtargets:
				xyCnt[xset[token['word']]] += 1
			else:
				xyCnt[yset[token['word']]] += 1
			colloc = True
			break

	xExist = False
	yExist = False
	colloc = False

print('Save ans to ./0556006_葉承翰_task2.txt')
with open('0556006_葉承翰_task2.txt', 'w') as f:
	l = len(lines)
	for i in range(3):
		px = float(xCnt[i]) / float(l)
		py = float(yCnt[i]) / float(l)
		pxy = float(xyCnt[i]) / float(l)
		f.write(xtargets[i] + '	' + pxtargets[i] + '	' + str(float(xCnt[i]) / float(l)) + '\n')
		f.write(ytargets[i] + '	' + pytargets[i] + '	' + str(float(yCnt[i]) / float(l)) + '\n')
		pmi = math.log2(pxy / (px * py))
		f.write(str(pmi) + '\n')
		f.write('\n')
