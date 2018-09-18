from pythonopensubtitles.settings import Settings
from xmlrpc.client import ServerProxy
import zlib, base64
from TReader import read
import json
import time
from random import *


def download(data, st):
	if st == 's':
		folder = 'simplified'
	elif st == 't':
		folder = 'traditional'
	maxCnt = -1
	maxSub = {}
	c = 0
	for subInfo in data:
		if int(subInfo['SubDownloadsCnt']) > maxCnt:
			maxCnt = int(subInfo['SubDownloadsCnt'])
			maxSub = subInfo

	if maxSub['SubFormat'] == 'srt':
		subId = maxSub['IDSubtitleFile']
		subEnc = maxSub['SubEncoding']
		if subEnc == '' or subEnc == 'Non-compliant Bi' or subEnc == 'Non-compliant GB' or subEnc == 'Unknown' or subEnc == 'BIG5-HKSCS:2004':
			subEnc = 'UTF-8'
		print(subEnc)

		subData = xmlrpc.DownloadSubtitles(token, [subId])
		encodedData = subData['data']
		for item in encodedData:
			decodedData = zlib.decompress(base64.b64decode(item['data']), 16 + zlib.MAX_WBITS).decode(subEnc, 'ignore')
			with open('./' + folder + '/' + movie + '.srt', 'w') as f:
				f.write(decodedData)
				print('Save to ./' + folder + '/' + movie + '.srt')
				c = 1
				b = True
	elif maxSub['SubFormat'] == 'ass':
		print('ass -> ' + movie)
		print('link: ' + maxSub['ZipDownloadLink'])
	
	return c, {'link': maxSub['ZipDownloadLink'], 'lang': folder}



xmlrpc = ServerProxy(Settings.OPENSUBTITLES_SERVER)
token = xmlrpc.LogIn('nctu', 'nctunlp', Settings.LANGUAGE, Settings.USER_AGENT)['token']
print('LogIn...')
print()
start = 1379
end = 2000

with open('movie2.txt', 'r') as targetsFile:
	lCnt = 0
	mCnt = 0
	assLinks = {}
	zhts = []
	for line in targetsFile:
		movie, movieT = read(line)
		lCnt += 1

		if lCnt > start and lCnt < end: 
			print('Download subtitle for ' + movie)
			print(lCnt)
			data = xmlrpc.SearchSubtitles(token, [{'query': movie, 'sublanguageid': 'chi'}])['data']
			if data:
				'''maxCnt = -1
				maxSub = {}
				for subInfo in data:
					if int(subInfo['SubDownloadsCnt']) > maxCnt:
						maxCnt = int(subInfo['SubDownloadsCnt'])
						maxSub = subInfo

				if maxSub['SubFormat'] == 'srt':
					subId = maxSub['IDSubtitleFile']
					subEnc = maxSub['SubEncoding']
					if subEnc == '' or subEnc == 'Non-compliant Bi':
						subEnc = 'UTF-8'
					print(subEnc)

					subData = xmlrpc.DownloadSubtitles(token, [subId])
					encodedData = subData['data']
					for item in encodedData:
						decodedData = zlib.decompress(base64.b64decode(item['data']), 16 + zlib.MAX_WBITS).decode(subEnc, 'ignore')
						with open('./simplified/' + movie + '.srt', 'w') as f:
							f.write(decodedData)
							print('Save to ./simplified/' + movie + '.srt')
							mCnt += 1
				else:
					print('ass -> ' + movie)
					print('link: ' + maxSub['ZipDownloadLink'])
					assLinks[movie] = maxSub['ZipDownloadLink']'''
				tempc, tempDic = download(data, 's')
				if tempc == 1:
					mCnt += tempc
				else:
					if tempDic:
						assLinks[movie] = tempDic
					else:
						print('None')
			else:
				#time.sleep(uniform(0, 2))
				data = xmlrpc.SearchSubtitles(token, [{'query': movie, 'sublanguageid': 'zht'}])['data']
				if data:
					tempc, tempDic = download(data, 't')
					if tempc == 1:
						mCnt += tempc
					else:
						if tempDic:
							assLinks[movie] = tempDic
						else:
							print('None')
				else:
					print('None')

			print()
		#time.sleep(uniform(3, 5))

	with open('assLinks.json', 'w') as f:
		json.dump(assLinks, f)
		print('Save to ./assLinks.json')

xmlrpc.LogOut(token)
print('LogOut')
print('----------------------------')
print('Total download: ' + str(mCnt))
print('Total movies:' + str(lCnt))
