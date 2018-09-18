from pythonopensubtitles.settings import Settings
from xmlrpc.client import ServerProxy
from imdb import IMDb
import os
import json
import time
from random import *


def getMostFreq(data):
	ids = {}
	for d in data:
		if d['IDMovieImdb'] in ids:
			ids[d['IDMovieImdb']] += 1
		else:
			ids[d['IDMovieImdb']] = 0
	ordered = [(k, ids[k]) for k in sorted(ids, key=ids.get, reverse=True)]
	return ordered[0][0]


savePath = './rating/'
saveFile = 'scores.json'

im = IMDb()
downMov = []
if os.path.exists('./newAllTitle.txt'):
	print('Load ./newAllTitle.txt')
	with open('./newAllTitle.txt', 'r') as f:
		for line in f:
			downMov.append(line.strip().split('	')[0])
else:
	print('Find files in ./backup')
	downMov = os.listdir('./backup')
	downMov = [m.split('.txt')[0] for m in downMov]
print()
scores = {}

xmlrpc = ServerProxy(Settings.OPENSUBTITLES_SERVER)
token = xmlrpc.LogIn('jerryNLP', 'jerry0531', Settings.LANGUAGE, Settings.USER_AGENT)['token']
print('LogIn...')
print()
missing = []
print('Load missing scores...')
allfile = os.listdir('./rating')
for l in allfile:
	if l[0].isdigit():
		missing.append(int(l.strip().split('.json')[0]))
		print(l.strip().split('.json')[0])
print()
print('Load ./rating/scoresT.json')
with open('./rating/scoresT.json', 'r') as f:
	scores = json.load(f)
print('Size ' + str(len(scores)))
print()

mCnt = 0
for movie in downMov:
	mCnt += 1
	if mCnt in missing:
		try:
			print('Find IMDb id for ' + movie)
			print('No.' + str(mCnt))
			data = xmlrpc.SearchSubtitles(token, [{'query': movie}])['data']
			if len(data) == 0:
				score = 0
				r = 0
				v = 0
				print('Status: No id')
				print('Rating: ')
				print('Votes: ')
			else:
				mId = getMostFreq(data)
				temp = im.get_movie(mId)
				if temp:
					score = temp['rating'] * math.log(temp['votes'], 10)
					r = temp['rating']
					v = temp['votes']
					print('Status: Get score')
					print('Rating: ' + str(temp['rating']))
					print('Votes: ' + str(temp['votes']))
				else:
					score = 0
					r = 0
					v = 0
					print('Status: No score')
					print('Rating: ')
					print('Votes: ')
			scores[movie] = {'score': score, 'r': r, 'v': v}
			print('Score: ' + str(score))
			print()
			if mCnt % 100 == 0:
				time.sleep(20)
				print('Sleeping...')
				print()
		except:
			print('Dump to ' + savePath + str(mCnt - 1) + '.json')
			with open(savePath + str(mCnt - 1) + '.json', 'w') as f:
				json.dump(scores, f)
			print('Write log to ./start.txt')
			with open('start.txt', 'w') as f:
				f.write(str(mCnt - 1))
			print()

with open(savePath + saveFile, 'w') as f:
	json.dump(scores, f)
	print('----------------------')
	print('Save to ' + savePath + saveFile)
