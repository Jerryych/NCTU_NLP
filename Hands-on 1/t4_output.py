import json
import numpy as np
import math
from pycorenlp import StanfordCoreNLP


bigram = {}
bigramO = {}



with open('t4_ans.txt', 'w') as out:
	with open('./Hands-on 1/task4.txt', 'r') as textFile:
		nlp = StanfordCoreNLP('http://localhost:9000')
		for line in textFile:
			lineOut = ''
			output = nlp.annotate(line.split('|')[1].rstrip(), properties={'annotators': 'parse', 'outputFormat': 'json'})
			sentences = output['sentences']
			for sentence in sentences:
				deps = sentence['basicDependencies']
				target = deps[0]['dependentGloss']
				temp = {}
				for dep in deps:
					if dep['governorGloss'] == target:
						temp[dep['dependent']] = dep['dependentGloss'].lower()
					temp[deps[0]['dependent']] = target.lower()

				sentenceOut = ''
				tempKey = sorted(temp)
				for order in tempKey:
					sentenceOut += temp[order] + ' '
				lineOut += sentenceOut

			out.write(lineOut + '\n')

	with open('simplified.txt', 'r') as inputFile:
		for line in inputFile:
			words = line.rstrip().split(' ')
			lineBi = zip(words, words[1:])
			for w1, w2 in lineBi:
				if w1 not in bigram:
					bigram[w1] = {}
					bigram[w1][w2] = 1
				else:	
					if w2 not in bigram[w1]:
						bigram[w1][w2] = 1
					else:
						bigram[w1][w2] += 1

	w1Sums = {}
	tolw1Sum = 0
	bigramNum = 0
	for w1, w2s in bigram.items():
		colSum = 0
		for w2, w2c in w2s.items():
			colSum += w2c
		for w2, w2c in w2s.items():
			w2s[w2] = float(w2c) / float(colSum)

		w1Sums[w1] = colSum
		tolw1Sum += colSum
		bigramNum += len(w2s)

	Hx = 0.0
	for w1, w1Sum in w1Sums.items():
		pw1 = float(w1Sum) / float(tolw1Sum)
		Hx += pw1 * math.log2(pw1)
	Hx *= -1

	HyGx = 0.0
	for w1, w2s in bigram.items():
		tempH = 0
		for w2, pw2 in w2s.items():
			tempH += pw2 * math.log2(pw2)
		tempH *= -1
		pw1 = float(w1Sums[w1]) / float(tolw1Sum)
		HyGx += pw1 * tempH

	HxAy = 0.0
	HxAy = Hx + HyGx

	out.write(str(bigramNum) + ',' + str(Hx) + ',' + str(HyGx) + ',' + str(HxAy) + '\n')
	del bigram

	with open('original.txt', 'r') as textFile:
		for line in textFile:
			words = line.rstrip().split(' ')
			lineBi = zip(words, words[1:])
			for w1, w2 in lineBi:
				if w1 not in bigramO:
                                        bigramO[w1] = {}
                                        bigramO[w1][w2] = 1
				else:
                                        if w2 not in bigramO[w1]:
                                                bigramO[w1][w2] = 1
                                        else:
                                                bigramO[w1][w2] += 1

	w1Sums = {}
	tolw1Sum = 0
	bigramNum = 0
	for w1, w2s in bigramO.items():
                colSum = 0
                for w2, w2c in w2s.items():
                        colSum += w2c
                for w2, w2c in w2s.items():
                        w2s[w2] = float(w2c) / float(colSum)

                w1Sums[w1] = colSum
                tolw1Sum += colSum
                bigramNum += len(w2s)

	HxO = 0.0
	for w1, w1Sum in w1Sums.items():
                pw1 = float(w1Sum) / float(tolw1Sum)
                HxO += pw1 * math.log2(pw1)
	HxO *= -1

	HyGxO = 0.0
	for w1, w2s in bigramO.items():
                tempH = 0
                for w2, pw2 in w2s.items():
                        tempH += pw2 * math.log2(pw2)
                tempH *= -1
                pw1 = float(w1Sums[w1]) / float(tolw1Sum)
                HyGxO += pw1 * tempH

	HxAyO = 0.0
	HxAyO = HxO + HyGxO

	out.write(str(bigramNum) + ',' + str(HxO) + ',' + str(HyGxO) + ',' + str(HxAyO) + '\n')
