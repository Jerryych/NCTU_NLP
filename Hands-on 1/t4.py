import json


files = ['m' + str(i) + '.json' for i in range(617)]
oriLines = []
with open('simplified.txt', 'w') as outputFile:

	for f in files:
		with open('./parsing_result/' + f, 'r') as movieFile:
			movieLines = json.load(movieFile)

		for line, sentences in movieLines.items():
			lineOutOri = ''
			lineOut = ''
			for sentence in sentences:
				deps = sentence['basicDependencies']
				target = deps[0]['dependentGloss']
				tempOri = {}
				temp = {}
				for dep in deps:
					tempOri[dep['dependent']] = dep['dependentGloss'].lower()
					if dep['governorGloss'] == target:
						temp[dep['dependent']] = dep['dependentGloss'].lower()
				tempOri[deps[0]['dependent']] = target.lower()
				temp[deps[0]['dependent']] = target.lower()

				sentenceOutOri = ''
				sentenceOut = ''
				'''tempOriKey = list(tempOri.keys())
				tempOriKey.sort()'''
				tempOriKey = sorted(tempOri)
				for order in tempOriKey:
					sentenceOutOri += tempOri[order] + ' '
				'''tempKey = list(temp.keys())
				tempKey.sort()'''
				tempKey = sorted(temp)
				for order in tempKey:
					sentenceOut += temp[order] + ' '
				lineOutOri += sentenceOutOri
				lineOut += sentenceOut
				
				'''outputFile.write(sentenceOut + '\n')
				oriLines.append(sentenceOutOri)'''

			outputFile.write(lineOut + '\n')
			oriLines.append(lineOutOri)

		print(f + ' done.')

print('generate simplified.txt ...')

with open('original.txt', 'w') as outputFile:
	for line in oriLines:
		outputFile.write(line + '\n')

print('generate original.txt ...')
