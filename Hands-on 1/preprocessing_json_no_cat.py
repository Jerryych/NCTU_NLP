'''
	2017 NCTU NLP course, lab1 preprocessing corpus.
	Dataset: cornell movie-dialogs corpus
	Tools: Stanford CoreNLP
	Author: Jerry

	This program is for generating POS tagging, Constituency parsing, Dependency parsing for every sentence in the corpus.
	No categorization on movie for each line in this program.
	Output files will be json files.
'''


from pycorenlp import StanfordCoreNLP
import json
import sys


nlp = StanfordCoreNLP('http://localhost:9000')
inputFile = open('cornell movie-dialogs corpus/movie_lines.txt', 'r', encoding='windows-1252')
conTree = {}
depTree = {}
posTags = {}
delimiter = ' +++$+++ '
keyD = '|'
c = 0


for line in inputFile:
	c = c + 1
	segs = line.split(delimiter)
	output = nlp.annotate(segs[4].rstrip(), properties={'annotators': 'pos, parse', 'outputFormat': 'json'})
	tempKey = segs[0] + keyD + segs[1] + keyD + segs[2] + keyD + segs[3]
	sc = 0
	for sen in output['sentences']:
		conTree[tempKey + keyD + str(sc)] = sen['parse']
		depTree[tempKey + keyD + str(sc)] = sen['basicDependencies']
		posTags[tempKey + keyD + str(sc)] = sen['tokens']
		sc = sc + 1

	print('\rAt line %d' % c, end='')
	#print('At line %d' % c, end='\r')


print()

with open('con_tree.json', 'w') as jsonFile:
        json.dump(conTree, jsonFile)
        print('Write data to con_tree.json')
with open('dep_tree.json', 'w') as jsonFile:
        json.dump(depTree, jsonFile)
        print('Write data to dep_tree.json')
with open('pos_tags.json', 'w') as jsonFile:
	json.dump(posTags, jsonFile)
	print('Write data to pos_tags.json')

print('done.')
inputFile.close()
