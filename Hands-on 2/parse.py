from pycorenlp import StanfordCoreNLP
import json
from TReader import read
from opencc import OpenCC


nlp = StanfordCoreNLP('http://localhost:9000')
occ = OpenCC('s2t')

with open('movie.txt', 'r') as targetsFile:
	targetsFile.readline()
	for line in targetsFile:
		movie, movieId = read(line)
		segments = []

		print('Read ./simplified/' + movie + '.txt')
		with open('./simplified/' + movie + '.txt', 'r') as movielines:
			for movieline in movielines:
				output = nlp.annotate(movieline.rstrip(), properties={'annotators': 'pos', 'pipelineLanguage': 'zh', 'outputFormat': 'json'})
				sentences = output['sentences']
				for sentence in sentences:
					tokens = sentence['tokens']
					for token in tokens:
						token['word'] = occ.convert(token['word'])
					segments.append(tokens)

		with open('./parsing_result/' + movie + '.json', 'w') as jsonFile:
			json.dump(segments, jsonFile)
			print('Save to ./parsing_result/' + movie + '.json')

		print()

