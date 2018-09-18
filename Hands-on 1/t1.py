import json
import math


files = ['m' + str(i) + '.json' for i in range(617)]
df = {}
wordList = []
N = 0

print('start counting df...')
for f in files:
	with open('./parsing_result/' + f, 'r') as movieFile:
		movieLines = json.load(movieFile)

	for line, sentences in movieLines.items():
		for sentence in sentences:
			tokens = sentence['tokens']
			for ws in tokens:
				word =  ws['word'].lower()
				wordList.append(word)
		wordSet = set(wordList)
		wordList = []
		for w in wordSet:
			if w not in df:
				df[w] = 1
			else:
				df[w] += 1
		N += 1

	print(f + ' done.')

print()
print('start computing idf...')
for word, c in df.items():
	df[word] = math.log(float(N) / float(c), 10)

orderedIdf = [(k, df[k]) for k in sorted(df, key=df.get, reverse=True)]
print('# of words: %d' % len(orderedIdf))
#idf300 = orderedIdf[0: 300]
idf300 = orderedIdf[55067: 55367]
print('select top 300 idf value word...done')
print()

print('write all word...')
with open('t1_all_word.json', 'w') as jsonFile:
	json.dump(orderedIdf, jsonFile)
print('write top 300 word...')
with open('t1_300.json', 'w') as jsonFile:
	json.dump(idf300, jsonFile)
