import os
from opencc import OpenCC
from t2s import *
from parsing_subtitle import *
from for_TFIDF import *
from tfidf import *
from title_embedding import *
from scoringFunc import *


modelPath = 'svr_aall.pkl'
inputPath = './input'
extraPath = './extracted'
candsPath = './candidates'
embedPath = './embeddings'


loadModel(modelPath)
occ = OpenCC('s2t')

t2s(inputPath)

# big head
print('Parsing subtitle...')
parsing(extraPath)
generatingPostxt()

# pan
print('Generating title candidates...')
gen_candidate_title(thr_tfidf_max=10.0, thr_tfidf_min=8.0, max_words_num=30)

# poop
print('Embedding...')
embeddingTask1(candsPath)

# scoring
moviesEmbs = os.listdir(embedPath)
moviesEmbs = [m.strip().split('.json')[0] for m in moviesEmbs]
print('Write to ./task1_group3.txt')
with open('./task1_group3.txt', 'w') as outfile:
	for mcs in moviesEmbs:
		maxScore = -1
		argmax = -1
		m, yfinal = scoring(embedPath + '/' + mcs + '.json')
		ml = len(m)
		for i in range(ml):
			#print(' Name: ' + m[i] + '	' + 'Score: ' + str(yfinal[i]))
			if yfinal[i] > maxScore:
				maxScore = yfinal[i]
				argmax = i
		for i in range(ml):
			if yfinal[i] == yfinal[argmax]:
				print(occ.convert(m[i]) + '     ' + str(yfinal[i]))
		outfile.write(mcs + '	' + occ.convert(m[argmax]) + '\n')
