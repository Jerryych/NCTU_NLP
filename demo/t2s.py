import pysrt
import os
from opencc import OpenCC


def t2s(infolder):
	occ = OpenCC('t2s')
	for f in os.listdir(infolder):
		if f.endswith('.srt'):
			movie = f.split('.srt')[0]

			print('Read ' + infolder + '/' + movie + '.srt')
			subs = pysrt.open(infolder + '/' + movie + '.srt')
			with open('./extracted/' + movie + '.txt', 'w') as f:
				print('T to S: ' + movie)
				for sub in subs:
					subSimplified = occ.convert(sub.text)
					f.write(subSimplified + '\n')
				print('Save to ./extracted/' + movie + '.txt')

		print()
