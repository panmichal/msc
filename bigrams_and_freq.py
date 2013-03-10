# -*- coding: utf-8 -*-
import os
import nltk
import sys
import re
import csv

FILTERED_INDEX = "filtered_texts.txt"

def write_csv(freq, output):
	writer = csv.writer(open(output, "w"))
	for bigram in freq:
		if bigram[1][0] > 10 and bigram[1][1] > 10:
			writer.writerow([bigram[0], bigram[1][0], bigram[1][1]])
		
def make_bigrams_from_file(relative_path, freq_dict):
	try:
		txt = open(relative_path)
	except:
		print "[CANNOT OPEN FILE] "	+ relative_path
		return
	tokens = []
	added_in_file = []
	for line in txt.readlines():
		if re.search('ó|ą|ę|ż|ź|ś|ń|[scdr]z|[sc]j', line):
			continue	
		tokens += nltk.WordPunctTokenizer().tokenize(line)
	bigrams = nltk.bigrams(tokens)
	#print "[bigrams %s] %s" % (len(bigrams), relative_path)
	for bigram in bigrams:
		bigram = bigram[0].strip() + ' ' + bigram[1].strip()
		if len(bigram) < 7:
			continue
		try:
			bigram.encode("ascii")
		except:
			"[NON-ASCII] " + bigram
			continue				
		freq_dict.setdefault(bigram, [0, 0])[0] += 1
		if 	bigram not in added_in_file:
			freq_dict[bigram][1] += 1
			added_in_file.append(bigram)	
			
count = 0
freq_dict = {}
if len(sys.argv) < 3:
	print "Parameters: path_to_dir|filter output_file"
	sys.exit()			
if sys.argv[1] == 'filtered':
	filtered_index = open(FILTERED_INDEX, 'a+')
	already_filtered = [path.split()[0] for path in filtered_index.readlines() if path.split()[1] == "1"]
	print len(already_filtered)
	for relative_file in already_filtered:
		make_bigrams_from_file(relative_file, freq_dict)
		count += 1
		print count
else:
	for root, dirs, files in os.walk(sys.argv[1]):
		for f in files:
			relative_path = root + "/" + f
			make_bigrams_from_file(relative_path, freq_dict)
			count +=1
			print count
sorted_freq = sorted(freq_dict.items(), key= lambda (k, v): v[0])
write_csv(sorted_freq, sys.argv[2])
