from pycorenlp import StanfordCoreNLP
import json
import os

def parsing(folderName):

	nlp = StanfordCoreNLP('http://localhost:9000')

	arr = os.listdir('./'+folderName) # extracted

	# print('arr : ', arr)

	save_path = './parsed_subtitle/'


	for movieName in arr:

		movieNameNoTxt = movieName.replace('.txt', '')

		#parsing the Chinese words
		afterParsed = {}

		parsetask = open(save_path+movieNameNoTxt+".json", 'w')
		# parsetask = os.path.join(save_path, movieNameNoTxt+".json")         

		with open('./'+folderName+'/'+movieName) as f:

			# toConvertLines = list(f)

			lines = list(f) 

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

			json.dump(afterParsed, parsetask)

