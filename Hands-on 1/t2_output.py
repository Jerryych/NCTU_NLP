from pycorenlp import StanfordCoreNLP
import json


linesWords = {}
lc = 0
nlp = StanfordCoreNLP('http://localhost:9000')
print('read task2.txt ...')
with open('Hands-on 1/task2.txt', 'r') as textFile:
	for line in textFile:
		linesWords[lc] = {}
		output = nlp.annotate(line.split('|')[1].rstrip(), properties={'annotators': 'parse', 'outputFormat': 'json'})
		sentences = output['sentences']
		for sentence in sentences:
			tokens = sentence['tokens']
			for ws in tokens:
				word = ws['word'].lower()
				pos = ws['pos']
				wp = word + '|' + pos
				if wp not in linesWords[lc]:
					linesWords[lc][wp] = 1
				else:
					linesWords[lc][wp] += 1
		lc += 1
	print('processing task1.txt lines done.')

with open('t2_300.json', 'r') as jsonFile:
	print('read t2_300.json ...')
	dims = json.load(jsonFile)

print('generate output file...')
with open('t2_ans.txt', 'w') as out:
	line1 = ''
	line2 = ''
	line3 = ''
	for dim in dims:
		wpp = dim[0].split('|')
		line1 += str(wpp[0]) + '|'
		line2 += str(wpp[1]) + '|'
		line3 += str(dim[1]) + ','

	line1 = line1[: -1]
	line2 = line2[: -1]
	line3 = line3[: -1]
	out.write(line1 + '\n')
	out.write(line2 + '\n')
	out.write(line3 + '\n')

	for id, lineWords in linesWords.items():
		lineOut = ''
		for dim in dims:
			if dim[0] in lineWords:
				tfidf = lineWords[dim[0]] * dim[1]
				lineOut += str(tfidf) + ','
			else:
				lineOut += str(0) + ','
		lineOut = lineOut[: -1]
		out.write(lineOut + '\n')
