import json
import pysrt


print('Read ./links.json')
with open('links.json', 'r') as f:
	links = json.load(f)
print('Save ans to ./0556006_葉承翰_task1.txt')
with open('0556006_葉承翰_task1.txt', 'w') as f:
	for movie, link in links.items():
		subs = pysrt.open('./traditional/' + movie + '.srt')
		f.write(movie + '	' + link + '	' + str(len(subs)) + '\n')

