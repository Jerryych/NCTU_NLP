import os
import json
from parsing_title import *
from title_embedding import *
from scoringFunc import *


modelPath = 'svr_aall.pkl'

loadModel(modelPath)

# big head
print('Prasing title...')
parsingtitle()

# poop
print('Embedding...')
embeddingTask2()

print('Write to ./task2_group3.txt')
with open('./task2_group3.txt', 'w') as outfile:
	m, yfinal = scoring('embeddings.json')
	mdic = {}
	ml = len(m)
	for i, sc in enumerate(yfinal):
		mdic[m[i]] = sc
	ordered = [(k, mdic[k]) for k in sorted(mdic, key=mdic.get, reverse=True)]
	with open('title_id.json', 'r') as f:
		ids = json.load(f)
	cnt = 0
	for movie, score in ordered:
		cnt += 1
		print(str(cnt) + '	' + ids[movie + '\n'] + '	' + movie + '	' + str(score))
		outfile.write(ids[movie + '\n'] + '\n')
