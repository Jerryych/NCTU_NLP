import pysrt
import os
from TReader import read
from opencc import OpenCC


occ = OpenCC('t2s')
folders = ['./simplified', './traditional']
for folder in folders:
	for f in os.listdir(folder):
		if f.endswith('.srt'):
			movie = f.split('.srt')[0]

			print('Read ' + folder + '/' + movie + '.srt')
			subs = pysrt.open(folder + '/' + movie + '.srt')
			with open('./extracted/' + movie + '.txt', 'w') as f:
				print('T to S: ' + movie)
				for sub in subs:
					subSimplified = occ.convert(sub.text)
					f.write(subSimplified + '\n')
				print('Save to ./extracted/' + movie + '.txt')

		print()
