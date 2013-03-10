import requests
import json
import urllib2
import urllib
import psycopg2
import time
import os
import httplib
import socket


def connect():
    conn = psycopg2.connect("dbname=polish_english user=postgres")

def main():
	phrases_file = open('phrases.txt', 'r')
	phrases = phrases_file.readlines()
	used_phrases_file= open('used_phrases_edu.txt', 'a+r')
	used_phrases = used_phrases_file.readlines();
	not_used_phrases = (set(phrases) - set(used_phrases))
	
	i = 0
	j = 0
	for phrase in not_used_phrases:
		directory = 'downloaded/edu_pl/phrase_' + phrase.strip()
		if not os.path.exists(directory):
			os.makedirs(directory)
		skip = 0	
		while (skip < 1000)	:
			print 'SKIP:' + str(skip)
			try:
				results = requests.get('https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Web?Query=%27' + phrase +'%20filetype%3apdf%20site%3aedu.pl%27&$top=50&$skip=' + str(skip) + '&$format=json', auth=('Vxbtruaz5tT9eNu0LuhSxuUQgso92B9DTWICaSPky/U=', 'Vxbtruaz5tT9eNu0LuhSxuUQgso92B9DTWICaSPky/U=')).json
			except:
				print "error occurred while querying Bing"
				continue
			for result in results['d']['results']:
				url = result['Url']
				i += 1
				j += 1
				print("[" + phrase.strip() + "]" + url)
				try:
					response = urllib2.urlopen(url, timeout=60)
				except socket.timeout:
					print "timeout"
					continue	
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
				output_path = 'downloaded/edu_pl/phrase_' + phrase.strip() + '/' + filename;
				if os.path.exists(output_path):
					print "File exists"
					continue		
				output = open(output_path,'w')
				try:
					output.write(response.read())
				except socket.timeout:
					print "timeout"
				except httplib.IncompleteRead:
					print "Incomplete read"	
				output.close()
				if (j == 100):
					#time.sleep(20)
					j = 0	
			skip += 50	
		used_phrases_file.write(phrase + "\n")	
		time.sleep(120)
if __name__ == '__main__':
  main()
