from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib
import numpy as np
import json


def tofloat(wordEmb):
	for movie, embeddings in wordEmb.items():
		for idx, emb in enumerate(wordEmb[movie]):
			for i, d in enumerate(emb):
				wordEmb[movie][idx][i] = float(d)


def padding(wordEmb):
	maxLen = -1
	for movie, embedding in wordEmb.items():
		if len(embedding) > maxLen:
			maxLen = len(embedding)
	pade = np.array([[0.0 for i in range(embLen)]])
	for movie, embedding in wordEmb.items():
		wordEmb[movie] = np.array(embedding).flatten()
		diff = maxLen - len(embedding)
		for i in range(diff):
			wordEmb[movie] = np.append(wordEmb[movie], pade)
	return wordEmb


def adding(wordEmb):
	for movie, embedding in wordEmb.items():
		temp = np.array(p.copy())
		for emb in embedding:
			temp += np.array(emb)
		wordEmb[movie] = np.array(temp)
	return wordEmb


embLen = 64
p = [0.0 for i in range(embLen)]
print('Load ./rating/scores.json')
with open('./rating/scores.json', 'r') as f:
	scores = json.load(f)
print()
print('Load ./movie_title_embedding.json')
with open('movie_title_embedding.json', 'r') as f:
	WE = json.load(f)
	print('	tofloat...')
	tofloat(WE)
	'''wordEmbedding = {}
	for m, e in WE.items():
		if p not in WE[m]:
			wordEmbedding[m] = e'''
	wordEmbedding = WE.copy()
	print('	padding...')
	wordEmb = padding(wordEmbedding.copy())
	print('	adding...')
	wordAdd = adding(wordEmbedding.copy())
print()

sk = set(list(scores.keys()))
ek = set(list(wordEmb.keys()))
inter = list(sk & ek)

print('SV Regression with padding...')
x = []
y = []

for movie in inter:
	if scores[movie]['score'] != 0:
		x.append(wordEmb[movie])
		y.append(scores[movie]['score'])
print('	x: ' + str(len(x)))
print('	x dim: ' + str(len(x[0])))
print('	y: ' + str(len(y)))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

svr = SVR(C=1.0, epsilon=0.1)
svr.fit(x_train, y_train)
print('Score: ' + str(svr.score(x_test, y_test)))
y_pred = svr.predict(x_test)
#for i, v in enumerate(y_pred):
#	print(str(v) + '        ' + str(y_test[i]))
print('MAE: ' + str(mean_absolute_error(y_test, y_pred)))

joblib.dump(svr, 'svr_p.pkl')
#load
#svr = joblib.load('svr_p.pkl')
print()

print('SV Regression with adding...')
x = []
y = []
m = []

for movie in inter:
	if scores[movie]['score'] != 0:
		m.append(movie)
		x.append(wordAdd[movie])
		y.append(scores[movie]['score'])
print('	x: ' + str(len(x)))
print('	x dim: ' + str(len(x[0])))
print('	y: ' + str(len(y)))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

svr = SVR(C=1.0, epsilon=0.1)
svr.fit(x_train, y_train)
print('Score: ' + str(svr.score(x_test, y_test)))
y_pred = svr.predict(x_test)
#for i, v in enumerate(y_pred):
#	print(str(v) + '	' + str(y_test[i]))
print('MAE: ' + str(mean_absolute_error(y_test, y_pred)))

joblib.dump(svr, 'svr_a.pkl')
#load
#svr = joblib.load('svr_a.pkl')
print()

print('Knn Regression with adding...')
print('	x: ' + str(len(x)))
print('	x dim: ' + str(len(x[0])))
print('	y: ' + str(len(y)))

kr = KNeighborsRegressor(n_neighbors=85, weights='distance')
kr.fit(x_train, y_train)
print('Score: ' + str(kr.score(x_test, y_test)))
y_pred = kr.predict(x_test)
for i, v in enumerate(y_pred):
	print(str(v) + '        ' + str(y_test[i]))
print('MAE: ' + str(mean_absolute_error(y_test, y_pred)))

joblib.dump(kr, 'kr_a.pkl')
#load
#kr = joblib.load('kr_a.pkl')

msd = {}	
ya_pred = kr.predict(x)
scoreDiff = np.array(y) - np.array(ya_pred)
for i, movie in enumerate(m):
	msd[movie] = scoreDiff[i]

print('Save to ./movie_score_diff.json')
with open('movie_score_diff.json', 'w') as f:
	json.dump(msd, f)
