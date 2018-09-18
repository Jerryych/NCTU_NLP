'''
	2017 NCTU NLP course, lab1 preprocessing corpus.
	Dataset: cornell movie-dialogs corpus
	Tools: Stanford CoreNLP
	Author: Jerry

	This program is for generating POS tagging, Constituency parsing, Dependency parsing for every sentence in the corpus.
	With categorization on movie for each line.
	Output files are in ./parsing_result, and each of which is a json file.
'''


from pycorenlp import StanfordCoreNLP
import json
import sys
import os


nlp = StanfordCoreNLP('http://localhost:9000')
inputFile = open('cornell movie-dialogs corpus/movie_lines.txt', 'r', encoding='windows-1252')
movies = {}
delimiter = ' +++$+++ '
keyD = '|'
c = 0
path = './parsing_result/'

if not os.path.exists(path):
	os.makedirs(path)


prevMovie = 'm0'
movies[prevMovie] = {}
for line in inputFile:
	c = c + 1
	segs = line.split(delimiter)

	if segs[2] not in movies:
		with open(path + prevMovie + '.json', 'w') as jsonFile:
			json.dump(movies[prevMovie], jsonFile)
			print('	Write data to ' + path + prevMovie + '.json')
		del movies[prevMovie]
		movies[segs[2]] = {}

	tempKey = segs[0] + keyD + segs[1] + keyD + segs[2] + keyD + segs[3]
	output = nlp.annotate(segs[4].rstrip(), properties={'annotators': 'parse', 'outputFormat': 'json'})
	movies[segs[2]][tempKey] = output['sentences']
	for sen in movies[segs[2]][tempKey]:
		del sen['enhancedDependencies']
		del sen['enhancedPlusPlusDependencies']

	prevMovie = segs[2]

	print('\rAt line %d' % c, end='')
	#print('At line %d' % c, end='\r')

with open(path + prevMovie + '.json', 'w') as jsonFile:
	json.dump(movies[prevMovie], jsonFile)
	print('	Write data to ' + path + prevMovie + '.json')
del movies[prevMovie]


print('done.')
inputFile.close()
