from pythonopensubtitles.settings import Settings
from pythonopensubtitles.utils import decompress
from xmlrpc.client import ServerProxy
import zlib, base64
from TReader import read
import json


xmlrpc = ServerProxy(Settings.OPENSUBTITLES_SERVER)
token = xmlrpc.LogIn('jerryNLP', 'jerry0531', Settings.LANGUAGE, Settings.USER_AGENT)['token']
print('LogIn...')
print()

with open('movie.txt', 'r') as targetsFile:
	links = {}
	targetsFile.readline()
	for line in targetsFile:
		movie, movieId = read(line)

		print('Download subtitle for ' + movie)
		data = xmlrpc.SearchSubtitles(token, [{'query': movie, 'sublanguageid': 'zht'}])['data']
		maxCnt = -1
		maxSub = {}
		for subInfo in data:
			if int(subInfo['SubDownloadsCnt']) > maxCnt:
				maxCnt = int(subInfo['SubDownloadsCnt'])
				maxSub = subInfo

		if maxSub['SubFormat'] == 'srt':
			links[movie] = maxSub['ZipDownloadLink']
			subId = maxSub['IDSubtitleFile']
			subEnc = maxSub['SubEncoding']
			if subEnc == '':
				subEnc = 'UTF-8'

			subData = xmlrpc.DownloadSubtitles(token, [subId])
			encodedData = subData['data']
			for item in encodedData:
				#decodedData = decompress(item['data'], subEnc)
				decodedData = zlib.decompress(base64.b64decode(item['data']), 16 + zlib.MAX_WBITS).decode(subEnc, 'ignore')
				with open('./traditional/' + movie + '.srt', 'w') as f:
					f.write(decodedData)
					print('Save to ./traditional/' + movie + '.srt')
		else:
			print('ass -> ' + movie)
			print('link: ' + maxSub['ZipDownloadLink'])

		print()

	with open('links.json', 'w') as f:
		json.dump(links, f)
		print('Save to ./links.json')

xmlrpc.LogOut(token)
print('LogOut')
