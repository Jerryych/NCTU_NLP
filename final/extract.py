import pysrt
import os
from TReader import read


for f in os.listdir('./simplified'):
	if f.endswith('.srt'):
		movie = f.split('.srt')[0]

		print('Read ./simplified/' + movie + '.srt')
		subs = pysrt.open('./simplified/' + movie + '.srt')
		with open('./extracted/' + movie + '.txt', 'w') as f:
			print('Extracting ' + movie)
			for sub in subs:
				f.write(sub.text + '\n')
			print('Save to ./extracted/' + movie + '.txt')

	print()
