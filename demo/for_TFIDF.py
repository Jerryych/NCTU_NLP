import json
import os

def generatingPostxt():

	arr = os.listdir('./parsed_subtitle')

	save_path = './postxt/'

	for movieName in arr:

		movieNameNoJson = movieName.replace('.json', '')

		each_movie_sub = open(save_path+movieNameNoJson+".txt", 'w')

		with open('./parsed_subtitle/'+movieNameNoJson+'.json') as subtitle:
			
			data = json.load(subtitle)

			print(''+movieNameNoJson+' : ', data)

			print(''+movieNameNoJson+' length : ', len(data))

			# for sentence in range(0, len(data)):

			keywords = {}
			keywords_POS = {}
			# unsimkeywords = {}

			redundant_checking = []

			for x in data.keys(): #each line

				keywords[x] = []
				keywords_POS[x] = []

				# unsimkeywords[x] = []

				index = data[x]

				print('index : ', index)

				if not index:
					continue

				try:
					checking = index[0]['basicDependencies'][0]['dependentGloss']
				except:
					continue

				rootvab = index[0]['basicDependencies'][0]['dependentGloss']

				dependent = 1
				lastdependent = 0
				rootvabdependent = 0

				if index[0]['basicDependencies'][0]['dependent'] != 1:
					rootvabdependent = index[0]['basicDependencies'][0]['dependent']

				try:

					newlist = index[0]['tokens']
					
					for dependent_dict in newlist:
						keywords[x].append(dependent_dict['word'])
						keywords_POS[x].append(dependent_dict['pos'])

						each_movie_sub.write(dependent_dict['word']+'\t')
						each_movie_sub.write(dependent_dict['pos']+'\n')

				except:
					continue


