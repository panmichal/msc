# -*- coding: utf-8 -*-
import os
import nltk
import sys
import re
import csv

FILTERED_INDEX = "filtered_texts.txt"

def write_csv(freq, output):
	writer = csv.writer(open(output, "w"))
	for token in freq:
		writer.writerow([token[0], token[1][0], token[1][1]])
		
def tokenize_file(relative_path, freq_dict):
	txt = open(relative_path)
	tokens = []
	added_in_file = []
	for line in txt.readlines():
		if re.search('ó|ą|ę|ż|ź|ś|ń', line):
			continue	
		tokens += nltk.WordPunctTokenizer().tokenize(line)
	print "[tokens %s] %s" % (len(tokens), relative_path)	
	for token in tokens:
		token = token.strip()
		if len(token) < 4:
			continue
		try:
			token.encode("ascii")
		except:
			"[NON-ASCII] " + token
			continue				
		freq_dict.setdefault(token, [0, 0])[0] += 1
		if 	token not in added_in_file:
			freq_dict[token][1] += 1
			added_in_file.append(token)	
			
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
		tokenize_file(relative_file, freq_dict)
		count += 1
		print count
else:
	for root, dirs, files in os.walk(sys.argv[1]):
		for f in files:
			relative_path = root + "/" + f
			tokenize_file(relative_path, freq_dict)
			count +=1
			print count
sorted_freq = sorted(freq_dict.items(), key= lambda (k, v): v[0])
write_csv(sorted_freq, sys.argv[2])
