'''
	2017 NCTU NLP course, lab1 preprocessing corpus.
	Dataset: cornell movie-dialogs corpus
	Tools: Stanford CoreNLP
	Author: Jerry

	This program is for generating POS tagging, Constituency parsing, Dependency parsing for every sentence in the corpus.
	No categorization on movie for each line in this program.
	Output files are txt files.
'''


from pycorenlp import StanfordCoreNLP
import json
import sys


nlp = StanfordCoreNLP('http://localhost:9000')
inputFile = open('cornell movie-dialogs corpus/movie_lines.txt', 'r', encoding='windows-1252')
outputCon = open('con_tree.txt', 'w')
outputDep = open('dep_tree.txt', 'w')
delimiter = ' +++$+++ '
c = 0


for line in inputFile:
	c = c + 1
	segs = line.split(delimiter)
	output = nlp.annotate(segs[4].rstrip(), properties={'annotators': 'pos, parse', 'outputFormat': 'json'})
	for sen in output['sentences']:
		outputCon.write(json.dumps(sen['parse']) + '\n')
		outputDep.write(json.dumps(sen['basicDependencies']) + '\n')

	print('\rAt line %d' % c, end='')
	#print('At line %d' % c, end='\r')


print()
inputFile.close()
outputCon.close()
outputDep.close()
