from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib
import numpy as np
import json


embLen = 64
p = [0.0 for i in range(embLen)]
svr = SVR(C=1.0, epsilon=0.1)


def tofloat(wordEmb):
	for movie, embeddings in wordEmb.items():
		for idx, emb in enumerate(wordEmb[movie]['embedding']):
			for i, d in enumerate(emb):
				wordEmb[movie]['embedding'][idx][i] = float(d)


def adding(wordEmbedding):
	wordEmb = {}
	charEmb = {}
	for movie, embedding in wordEmbedding.items():
		temp = np.array(p.copy())
		for emb in embedding['embedding']:
			temp += np.array(emb)
		wordEmb[movie] = np.array(temp)
		charEmb[movie] = embedding['score']
	return wordEmb, charEmb


def loadModel(model):
	global svr
	print('Load model from ' + './' + model)
	svr = joblib.load(model)
	print()


def scoring(infile):
	global svr
	print('	Load ' + infile)
	with open(infile, 'r') as f:
		WE = json.load(f)
		print('		tofloat...')
		tofloat(WE)
		print('		adding...')
		wordAdd, charEmb = adding(WE.copy())
	print()

	print('	SV Regression with adding...')
	x = []
	ps = []
	m = []

	for movie, v in wordAdd.items():
		m.append(movie)
		x.append(v)
		ps.append(charEmb[movie])
	print('		x: ' + str(len(x)))
	print('		x dim: ' + str(len(x[0])))
	print()

	y = svr.predict(x)
	yfinal = y + np.array(ps)
	return m, yfinal
