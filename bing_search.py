import requests
import json
import urllib2
import urllib
import psycopg2
import time
import os
import httplib

def connect():
    conn = psycopg2.connect("dbname=polish_english user=postgres")

def main():
	phrases_file = open('phrases.txt', 'r')
	phrases = phrases_file.readlines()
	used_phrases_file= open('used_phrases.txt', 'a+r')
	used_phrases = used_phrases_file.readlines();
	not_used_phrases = (set(phrases) - set(used_phrases))
	
	conn = psycopg2.connect("dbname=polish_english user=postgres")
	cur = conn.cursor()
	i = 0
	j = 0
	for phrase in not_used_phrases:
		directory = 'downloaded/phrase_' + phrase.strip()
		if not os.path.exists(directory):
			os.makedirs(directory)
		skip = 0	
		while (skip < 1000)	:
			print 'SKIP:' + str(skip)
			results = requests.get('https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Web?Query=%27' + phrase +'%20site%3apl%27&$top=50&$skip=' + str(skip) + '&$format=json', auth=('Nr11EnLILZ3as4h88CL4NhxYRiSmlsrnJFMH6KqBpbg=', 'Nr11EnLILZ3as4h88CL4NhxYRiSmlsrnJFMH6KqBpbg=')).json
			for result in results['d']['results']:
				url = result['Url']
				i += 1
				j += 1
				print(url)
				try:
					response = urllib2.urlopen(url)
				except urllib2.HTTPError:
					print "HTTPError"
					continue
				except ValueError:
					print "Value error"
					continue
				except urllib2.URLError:
					print "URLError"
					continue
				except:
					print "Unrecognized error"
					continue				
				if (url.split('/')[-1] != ''):
					filename = url.split('/')[-1]
				else:
					filename = url.split('/')[-2]	
				
				if (len(filename) > 128):
					filename = filename[:128]	
				output = open('downloaded/phrase_' + phrase.strip() + '/' + filename,'w')
				try:
					output.write(response.read())
				except httplib.IncompleteRead:
					print "Incomplete read"	
				output.close()
				cur.execute("INSERT INTO document (link, path) VALUES (%s, %s)", (url, filename))
				if (i == 10):
					conn.commit()
					i = 0;
				if (j == 100):
					#time.sleep(20)
					j = 0	
			skip += 50	
		used_phrases_file.write(phrase + "\n")	
		time.sleep(120)
if __name__ == '__main__':
  main()
