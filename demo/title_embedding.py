import gensim
import os
import json

def embeddingTask1(infolder):

	print('task1 before loading')

	# load the model
	model = gensim.models.KeyedVectors.load_word2vec_format('news_12g_baidubaike_20g_novel_90g_embedding_64.bin',binary=True)
	# load the letter score
	with open('letterDict.json') as json_file:
		letterScores = json.load(json_file)

	print('task1 after loading')

	# symbol 
	symbol = ['?','!','.','-','《','》','...','...?','/','(',')','~','"',':','•','♪','<','>','「','」','，','：',',','”','..?','“','”','..','·','~~~']

	# word not found list
	zero = []
	for x in range(64):
		zero.append(0)

	for file in os.listdir(infolder):
		if file.endswith(".txt"):

			titleZeroWords = {}
			titleZeroLetters = {}
			# read the word
			inputfile = open(infolder + '/' + file,'r')
			filename = file.replace('txt','')
			output_filename = "embeddings/"+filename+"json"
			outputfile = open(output_filename,'w')

			word_embedded = {}
			for word in inputfile:
				word = word.strip('\n')
				# words[0] is moevie title
				words = word.split('\t')
				embedding_score = {} # store the embedding result and score of each movie
				# word embedding
				vectors = []  # store the embedding
				zeroWords = [] # store the word which embedding cannot find
				zeroLetters = [] # store the leeter which embedding cannot find
				#print('movie title '+str(words[0]))
				titles = words[1].split(' ')
				score = 0
				if(len(titles)!=1):
					for element in titles:
						if(element!=titles[len(titles)-1]):
							try:
								vectors.append(model[element])
							except KeyError:
								zeroWords.append(element)
								vectors.append(zero)
								for letter in element:
									zeroLetters.append(letter)
									try:
										score += letterScores[letter]
									except KeyError:
										x = 1
					# store the word not found in dict by each movie
					titleZeroWords[words[0]] = zeroWords
					titleZeroLetters[words[0]] = zeroLetters
					vector_result = []
					for vector in vectors:
						temp = []
						for value in vector:
							temp.append(str(value).strip('\n'))
						vector_result.append(temp)	
					if(len(vector_result)!=0):
						embedding_score['embedding'] = vector_result
						embedding_score['score'] = score
						word_embedded[words[0]] = embedding_score

			json_data = json.dump(word_embedded,outputfile)


def embeddingTask2():
	# load the model
	model = gensim.models.KeyedVectors.load_word2vec_format('news_12g_baidubaike_20g_novel_90g_embedding_64.bin',binary=True)
	# load the letter score
	with open('letterDict.json') as json_file:
		letterScores = json.load(json_file)

	# symbol 
	symbol = ['?','!','.','-','《','》','...','...?','/','(',')','~','"',':','•','♪','<','>','「','」','，','：',',','”','..?','“','”','..','·','~~~']

	# word not found list
	zero = []
	for x in range(64):
		zero.append(0)

	titleZeroWords = {}
	titleZeroLetters = {}
	# read the word
	input_filename = 'input_parsed.txt'
	inputfile = open(input_filename,'r')
	output_filename = 'embeddings.json'
	outputfile = open(output_filename,'w')

	word_embedded = {}
	for word in inputfile:
		word = word.strip('\n')
		# words[0] is moevie title
		words = word.split('\t')
		embedding_score = {} # store the embedding result and score of each movie
		# word embedding
		vectors = []  # store the embedding
		zeroWords = [] # store the word which embedding cannot find
		zeroLetters = [] # store the leeter which embedding cannot find
		#print('movie title '+str(words[0]))
		titles = words[1].split(' ')
		score = 0
		if(len(titles)!=1):
			for element in titles:
				if(element!=titles[len(titles)-1]):
					try:
						vectors.append(model[element])
					except KeyError:
						zeroWords.append(element)
						vectors.append(zero)
						for letter in element:
							zeroLetters.append(letter)
							try:
								score += letterScores[letter]
							except KeyError:
								x = 1
			# store the word not found in dict by each movie
			titleZeroWords[words[0]] = zeroWords
			titleZeroLetters[words[0]] = zeroLetters
			vector_result = []
			for vector in vectors:
				temp = []
				for value in vector:
					temp.append(str(value).strip('\n'))
				vector_result.append(temp)	
			if(len(vector_result)!=0):
				embedding_score['embedding'] = vector_result
				embedding_score['score'] = score
				word_embedded[words[0]] = embedding_score

	json_data = json.dump(word_embedded,outputfile)
