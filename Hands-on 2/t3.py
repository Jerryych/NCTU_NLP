from bs4 import BeautifulSoup
from pycorenlp import StanfordCoreNLP
from opencc import OpenCC


nlp = StanfordCoreNLP('http://localhost:9000')


occ = OpenCC('t2s')
occ2 = OpenCC('s2t')
soup = BeautifulSoup(open('table.html', 'r'), 'html.parser')

print('Parse html file')
out = soup.select('tbody > tr > td')
names = []
l = len(out)
for i in range(1, l, 6):
	names.append(out[i].string)

pattern = {}
moviePOS = {}

print('Count patterns')
for name in names:
	output = nlp.annotate(occ.convert(name.string.rstrip()), properties={'annotators': 'pos', 'pipelineLanguage': 'zh', 'outputFormat': 'json'})
	sentences = output['sentences']
	for sentence in sentences:
		tokens = sentence['tokens']
		p = ''
		for token in tokens:
			token['word'] = occ2.convert(token['word'])
			p += token['pos'] + '|'

		p = p[: -1]
		if p in pattern:
			pattern[p] += 1
		else:
			pattern[p] = 1

		if p in moviePOS:
			moviePOS[p].append(name.string)
		else:
			moviePOS[p] = []

ordered = [(k, pattern[k]) for k in sorted(pattern, key=pattern.get, reverse=True)]
top3 = ordered[:3]

print('Save ans to ./0556006_葉承翰_task3.txt')
with open('0556006_葉承翰_task3.txt', 'w') as f:
	for p, cnt in top3:
		f.write('(' + p.replace('|', ', ') + ')	' + str(cnt) + '	')
		ms = moviePOS[p]
		s = ''
		for m in ms:
			s += m + '	'
		s = s[: -1]
		f.write(s + '\n')
