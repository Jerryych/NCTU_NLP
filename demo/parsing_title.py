from pycorenlp import StanfordCoreNLP
from opencc import OpenCC

import json
import os

def parsingtitle():

	nlp = StanfordCoreNLP('http://localhost:9000')

	file = 'input.txt'

	movieNameNoTxt = file.replace('.txt', '')

	#parsing the Chinese words
	afterParsed = {}

	outputfile = open("input_parsed.txt", 'w')        

	title_idfile = open("title_id.json", 'w')        


	with open(file) as f:

		toIntergrate = list(f)

		openCC = OpenCC('t2s')

		title_id = {}

		lines = []
		linesEng = []
		for titleEngChi in toIntergrate:
			# Eng = titleEngChi.split('\t')[0]
			_id = titleEngChi.split('\t')[0]
			Chi = titleEngChi.split('\t')[1]

			s_Chi = openCC.convert(Chi)

			lines.append(s_Chi)

			title_id[s_Chi] = _id
			# linesEng.append(Eng)

		# lines = list(f) 

		json.dump(title_id, title_idfile)

		for sentences in range(0, len(lines)):
			try:

				print("length : ", len(lines[sentences]))
				# print(type(lines[sentences]))
				
				output = nlp.annotate(lines[sentences], properties={'annotators': 'tokenize,ssplit,pos,depparse,parse','outputFormat': 'json'})

				print("output : ",output)
				print(sentences," : ",output['sentences'])

				# print("Num : ", len(output['sentences']))
				
				subsentences = []
				for index in range(0, len(output['sentences'])):
					parsing_dict = {}
					# print("index : ", output['sentences'][index]['parse'])

					parsing_dict['index'] = index
					# parsing_dict['lineID'] = sublinessentences[0]


					# for subindex in range(0, len(list(output['sentences'][index]['tokens']))):
					# 	output['sentences'][index]['tokens'][subindex]['word'] = openCC2.convert(output['sentences'][index]['tokens'][subindex]['word'])

					parsing_dict['tokens'] = list(output['sentences'][index]['tokens'])

					
					# output['sentences'][index]['parse'] = openCC2.convert(output['sentences'][index]['parse'])

					parsing_dict['parse'] = output['sentences'][index]['parse']

					
					# for subindex in range(0, len(list(output['sentences'][index]['basicDependencies']))):
					# 	output['sentences'][index]['basicDependencies'][subindex]['governorGloss'] = openCC2.convert(output['sentences'][index]['basicDependencies'][subindex]['governorGloss'])
					# 	output['sentences'][index]['basicDependencies'][subindex]['dependentGloss'] = openCC2.convert(output['sentences'][index]['basicDependencies'][subindex]['dependentGloss'] )

					parsing_dict['basicDependencies'] = list(output['sentences'][index]['basicDependencies'])

					print("parsing_dict : ", parsing_dict)

					subsentences.append(parsing_dict)

					# sentences = sentences + 4

				afterParsed[str(sentences)] = subsentences

			except:
				print('Error')

			# json.dump(afterParsed, parsetask)

			# afterParsed get the title
			keywords = {}
			unsimkeywords = {}

			for x in afterParsed.keys(): #each line
				# print('afterParsed[x][] : ', afterParsed[x])

				# linewithsubsentence = list(afterParsed[x])
				keywords[x] = []
				unsimkeywords[x] = []
				# print('linewithsubsentence : ', linewithsubsentence)
				for index in afterParsed[x]: #each subline
					# print('index[basicDependencies] : ', index['basicDependencies'])
					
					# print('index[basicDependencies][0] : ', index['basicDependencies'][0])

					rootvab = index['basicDependencies'][0]['dependentGloss']

					# keywords[x].append(rootvab)

					dependent = 1
					lastdependent = 0
					rootvabdependent = 0

					if index['basicDependencies'][0]['dependent'] != 1:
						rootvabdependent = index['basicDependencies'][0]['dependent']
						# print(index['basicDependencies'][0]['dependentGloss'])

					# order = 1
					# for indexofVab in range(0,len(index['basicDependencies'])):
					try:

						newlist = sorted(index['basicDependencies'], key=lambda k: k['dependent']) 
						
						for dependent_dict in newlist:
							unsimkeywords[x].append(dependent_dict['dependentGloss'])

					except:
						continue

			# print("unsimkeywords : ", unsimkeywords)

			print('unsimkeywords x : ', unsimkeywords[str(sentences)])


			bool_keyword = False

			# checking all the keyword is null or not
			for keyword in unsimkeywords[str(sentences)]:
				if (keyword > u'\u4e000' and keyword < u'\u9fff'):
					bool_keyword = bool_keyword or True
					break
				else:
					bool_keyword = bool_keyword or False

			if bool_keyword:

				origin = lines[sentences].replace('\n','')

				outputfile.write(origin+'\t')

				for keyword in unsimkeywords[str(sentences)]:
					if (keyword > u'\u4e000' and keyword < u'\u9fff'):
						outputfile.write(keyword+' ')

				outputfile.write('\n')



