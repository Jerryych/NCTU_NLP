import json
from numpy import linalg as la
import numpy as np
import math


files = ['m' + str(i) + '.json' for i in range(6, 10)]
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
dotV = np.dot(mR, mR.T)
for i, vec in enumerate(moviesRep):
	norm = la.norm(vec)
	dotV[i, :] /= norm
	dotV[:, i] /= norm

maximum = -1
imax = 0
for i in range(len(files)):
	for j in range(i + 1, len(files)):
		if dotV[i, j] > maximum:
			maximum = dotV[i, j]
			imax = i

argmin = np.argmin(dotV[imax, :])
top3 = [f for i, f in enumerate(files) if i != argmin]
last1 = files[argmin]

print('generate output file...')
with open('t3_1_ans.txt', 'w') as out:  
	line1 = ''
	tmpN = {}
	with open('cornell movie-dialogs corpus/movie_titles_metadata.txt', 'r', encoding='windows-1252') as nameFile:
		for line in nameFile:
			segs = line.split(' +++$+++ ')
			tmpN[segs[0]] = segs[1]
	for m in top3:
		line1 += tmpN[m[: -5]] + '|'
	line1 = line1[: -1]
	out.write(line1 + '\n')

	line2 = ''
	for dim in dims:
		line2+= str(dim[0]) + '|'
	line2 = line2[: -1]
	out.write(line2 + '\n')

	line3To5 = ''
	for m in top3:
		vec = moviesRep[files.index(m)]
		for dV in vec:
			line3To5 += str(dV) + ','
		line3To5 = line3To5[: -1]
		line3To5 += '\n'
	out.write(line3To5)

	line6 = tmpN[last1[: -5]]
	out.write(line6 + '\n')

	line7 = ''
	vec = moviesRep[files.index(last1)]
	for dV in vec:
		line7 += str(dV) + ','
	line7 = line7[: -1]
	line7 += '\n'
	out.write(line7)
'''
print('computing centers and distance...')
center = np.array([0.0 for i in range(300)])
for vec in moviesRep:
	center += np.array(vec)
center = center / 617.0

movieDis = {}
i = 0
for vec in moviesRep:
	movieDis[i] = np.dot(center, np.array(vec)) / (la.norm(center) * la.norm(np.array(vec)))
	i += 1

orderedDis = [(k, movieDis[k]) for k in sorted(movieDis, key=movieDis.get, reverse=True)]
top3 = orderedDis[:3]
last1 = orderedDis[-1]

print('generate output file...')
with open('t3_1_ans.txt', 'w') as out:	
	line1 = ''
	for id, dis in top3:
		line1 += 'm' + str(id) + '|'
	out.write(line1 + '\n')

	line2 = ''
	for dim in dims:
		line2+= str(dim[0]) + '|'
	out.write(line2 + '\n')

	line3To5 = ''
	for id, dis in top3:
		vec = moviesRep[id]
		for dV in vec:
			line3To5 += str(dV) + '|'
		line3To5 += '\n'
	out.write(line3To5)

	line6 = 'm' + str(last1[0])
	out.write(line6 + '\n')

	line7 = ''
	vec = moviesRep[last1[0]]
	for dV in vec:
		line7 += str(dV) + '|'
	line7 += '\n'
	out.write(line7)
'''
'''
i = 0
for vec in moviesRep:
	norm = la.norm(vec)
	dot1[i, :] = dot1[:, i] / norm
'''
