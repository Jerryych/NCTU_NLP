import json
from numpy import linalg as la
import numpy as np
import math
from sklearn.cluster import KMeans
from collections import deque


files = ['m' + str(i) + '.json' for i in range(617)]
movies = {}

for f in files:
	with open('./parsing_result/' + f, 'r') as movieFile:
		movieLines = json.load(movieFile)

	movies[f] = {}

	for line, sentences in movieLines.items():
		for sentence in sentences:
			tokens = sentence['tokens']
			for ws in tokens:
				word = ws['word'].lower()
				if word not in movies[f]:
					movies[f][word] = 1
				else:
					movies[f][word] += 1

	print(f + ' done.')

with open('t1_300.json', 'r') as jsonFile:
	print('read t1_300.json ...')
	dims = json.load(jsonFile)

print('generate movie representation...')
tempMovies = []
for mf in files:
	tempMovies.append(movies[mf])
tempMovies = zip(files, tempMovies)
moviesRep = []
mc = 0
for movie, words in tempMovies:
	moviesRep.append([])
	for dim in dims:
		if dim[0] in words:
			tfidf = words[dim[0]] * dim[1]
			moviesRep[mc].append(tfidf)
		else:
			moviesRep[mc].append(0)

	mc += 1

mR = np.array(moviesRep)

print('clustering...')
depth = 5
times = math.pow(2, depth - 1)
t = 1
nQueue = deque()
nQueue.append([i for i in range(617)])
cQueue = deque()
cQueue.append(moviesRep)

while t < times:
	tN = nQueue.popleft()
	tC = cQueue.popleft()
	kmeans = KMeans(n_clusters=2, random_state=0).fit(tC)
	assignments = kmeans.labels_
	labels = set(assignments)
	sepN = []
	sepC = []
	for l in labels:
		sepN.append([])
		sepC.append([])
	for idx, assign in enumerate(assignments):
		sepN[assign].append(tN[idx])
		sepC[assign].append(tC[idx])
	for l in labels:
		nQueue.append(sepN[l])
		cQueue.append(sepC[l])
	t += 1

print('generate output file...')
with open('TD_clustering.txt', 'w') as out:  
	line1 = ''
	tmpN = {}
	with open('cornell movie-dialogs corpus/movie_titles_metadata.txt', 'r', encoding='windows-1252') as nameFile:
		for line in nameFile:
			segs = line.split(' +++$+++ ')
			tmpN[segs[0]] = segs[1]
	for idx, cluster in enumerate(nQueue):
		out.write(str(idx) + '\n')
		for mid in cluster:
			out.write(tmpN['m' + str(mid)] + '\n')
		
