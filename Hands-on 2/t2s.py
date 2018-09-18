import pysrt
from TReader import read
from opencc import OpenCC


occ = OpenCC('t2s')
with open('movie.txt', 'r') as targetsFile:
	targetsFile.readline()
	for line in targetsFile:
		movie, movieId = read(line)

		if movie != '"Star Wars: The Clone Wars" Conspiracy':

			print('Read ./traditionl/' + movie + '.srt')
			subs = pysrt.open('./traditional/' + movie + '.srt')
			with open('./simplified/' + movie + '.txt', 'w') as f:
				print('T to S: ' + movie)
				for sub in subs:
					subSimplified = occ.convert(sub.text)
					f.write(subSimplified + '\n')
				print('Save to ./simplified/' + movie + '.txt')

		print()
