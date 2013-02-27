from google import search
import urllib2
import urllib
import psycopg2
import time
import os

def connect():
    conn = psycopg2.connect("dbname=polish_english user=postgres")

def main():
	phrases_file = open('phrases.txt', 'r')
	phrases = phrases_file.readlines()
	used_phrases_file= open('used_phrases_edu.txt', 'a+r')
	used_phrases = used_phrases_file.readlines();
	not_used_phrases = (set(phrases) - set(used_phrases))
	
	conn = psycopg2.connect("dbname=polish_english user=postgres")
	cur = conn.cursor()
	i = 0
	j = 0
	for phrase in not_used_phrases:
		directory = 'downloaded/edu_pl/' + phrase.strip()
		if not os.path.exists(directory):
			os.makedirs(directory)
		for url in search('site:edu.pl filetype:pdf ' + phrase.strip(), stop=2000):
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
			output = open('downloaded/edu_pl/' + phrase.strip() + '/' + filename,'w')
			output.write(response.read())
			output.close()
			cur.execute("INSERT INTO document (link, path) VALUES (%s, %s)", (url, filename))
			if (i == 10):
				conn.commit()
				i = 0;
			if (j == 100):
				time.sleep(20)
				j = 0	
		used_phrases_file.write(phrase + "\n")	
		time.sleep(1200)
if __name__ == '__main__':
  main()
