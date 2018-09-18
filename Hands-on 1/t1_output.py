from pycorenlp import StanfordCoreNLP
import json


linesWords = {}
lc = 0
nlp = StanfordCoreNLP('http://localhost:9000')
print('read task1.txt...')
with open('Hands-on 1/task1.txt', 'r') as textFile:
	for line in textFile:
		linesWords[lc] = {}
		output = nlp.annotate(line.split('|')[1].rstrip(), properties={'annotators': 'parse', 'outputFormat': 'json'})
		sentences = output['sentences']
		for sentence in sentences:
			tokens = sentence['tokens']
			for ws in tokens:
				word = ws['word'].lower()
				if word not in linesWords[lc]:
					linesWords[lc][word] = 1
				else:
					linesWords[lc][word] += 1
		lc += 1
	print('processing task1.txt lines done.')

with open('t1_300.json', 'r') as jsonFile:
	print('read t1_300.json ...')
	dims = json.load(jsonFile)

print('generate output file...')
with open('t1_ans.txt', 'w') as out:
	line1 = ''
	line2 = ''
	for dim in dims:
		line1 += str(dim[0]) + '|'
		line2 += str(dim[1]) + ','

	line1 = line1[: -1]
	line2 = line2[: -1]
	out.write(line1 + '\n')
	out.write(line2 + '\n')

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
