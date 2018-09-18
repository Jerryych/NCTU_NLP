from bs4 import BeautifulSoup
from math import log
from pycorenlp import StanfordCoreNLP

import re
import requests
import time

#nlp = StanfordCoreNLP('http://localhost:9000')

#'&start=20'
pageUrl = '&start='

storing = open('douban_booktitle.txt', 'w')
# 
pageNum = 0

literatureList = ['中国文学', '外国文学', '日本文学', '外国名著']

titleList = []
scoreList = []
max_score = 0

for literature in literatureList:

	for pageNum in range(0, 100):

		url = "https://book.douban.com/tag/"+ literature +"?type=S"

		time.sleep (500.0 / 1000.0);

		if pageNum != 0:
			url = url + pageUrl + str(pageNum * 20)

		try:

			page = requests.get(url)

			soup = BeautifulSoup(page.text, 'html.parser')

			# print(soup.prettify())

			itemList = soup.find_all(class_='subject-item')

			# print(itemList)

			for item in itemList:

				info = item.find(class_='info')

				# print(info)

				#dealing with the title
				title_noise = info.find('h2')

				title = title_noise.find('a').text.strip()

				title = title.replace('\n','')

				re.sub(r"[\(\[].*?[\)\]]", "", title)

				# title = re.sub(r'\(.*\)','',title)

				title = title.split('（')[0]

				title = title.split(':')[0]

				title = title.strip()

				print(title)

				rating = info.find(class_='rating_nums').text

				print(rating)

				people_review = info.find(class_='pl').text

				people_review = people_review.split('人')[0].replace('(','').strip()

				print(people_review)

				if "精选集" not in title and "系列" not in title and not title.endswith('选'):
					score = float(rating)*log(int(people_review), 10)

					titleList.append(title)
					scoreList.append(score)

					if score > max_score:
						max_score = score

					# storing.write(title+'\t'+str(score)+'\n')
		
		except:
			print('Not found')


# storing.write(str(max_score)+'\n')

# storing.write(max_score+'\n')
for index in range(len(titleList)):

	storing.write(titleList[index]+'\t') #+str(normalized)+'\n'

	normalized = float(scoreList[index]/max_score)

	storing.write(str(normalized)+'\n')
	
'''
	try:

		print("length : ", len(titleList[index]))
		# print(type(titleList[index]))
		
		output = nlp.annotate(titleList[index], properties={'annotators': 'tokenize,ssplit,pos,depparse,parse','outputFormat': 'json'})

		print("output : ",output)
		print(sentences," : ",output['sentences'])

		# print("Num : ", len(output['sentences']))
		
		subsentences = []
		for index2 in range(0, len(output['sentences'])):
			parsing_dict = {}
			# print("index2 : ", output['sentences'][index2]['parse'])

			parsing_dict['index2'] = index2
			# parsing_dict['lineID'] = sublinessentences[0]


			# for subindex in range(0, len(list(output['sentences'][index2]['tokens']))):
			# 	output['sentences'][index2]['tokens'][subindex]['word'] = openCC2.convert(output['sentences'][index2]['tokens'][subindex]['word'])

			parsing_dict['tokens'] = list(output['sentences'][index2]['tokens'])

			
			# output['sentences'][index2]['parse'] = openCC2.convert(output['sentences'][index2]['parse'])

			parsing_dict['parse'] = output['sentences'][index2]['parse']

			
			# for subindex in range(0, len(list(output['sentences'][index2]['basicDependencies']))):
			# 	output['sentences'][index2]['basicDependencies'][subindex]['governorGloss'] = openCC2.convert(output['sentences'][index2]['basicDependencies'][subindex]['governorGloss'])
			# 	output['sentences'][index2]['basicDependencies'][subindex]['dependentGloss'] = openCC2.convert(output['sentences'][index2]['basicDependencies'][subindex]['dependentGloss'] )

			parsing_dict['basicDependencies'] = list(output['sentences'][index2]['basicDependencies'])

			print("parsing_dict : ", parsing_dict)

			subsentences.append(parsing_dict)

			# sentences = sentences + 4

		# afterParsed[str(sentences)] = subsentences

		# storing.write(titleList[index]+'\t'+str(normalized)+'\n')

		for title_word in subsentences:
			storing.write(title_word + " ")

		normalized = float(scoreList[index]/max_score)

		storing.write('\t'+str(normalized)+'\n')

	except:
	
		print('Error')
'''

