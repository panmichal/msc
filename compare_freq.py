from __future__ import division
import sys

PL_FILE = "freq_edu_pl_ascii.csv"
EN_FILE = "freq_ac_uk_ascii.csv"


K = 50

if len(sys.argv) < 3 or sys.argv[1] not in ['pl-en', 'en-pl']:
	print "Wrong parameters"
	sys.exit()
	
OUT_FILE = sys.argv[2]	

freq_list_pl = [line.split(',') for line in open(PL_FILE).readlines() if len(line.split(',')) == 3]
freq_list_en = [line.split(',') for line in open(EN_FILE).readlines() if len(line.split(',')) == 3]

freq_dict_pl = {}
for l in freq_list_pl:
	freq_dict_pl.setdefault(l[0], [0, 0])[0] += int(l[1])
	freq_dict_pl[l[0]][1] += int(l[2]) 
	
freq_dict_en = {}
for l in freq_list_en:
	freq_dict_en.setdefault(l[0], [0, 0])[0] += int(l[1])
	freq_dict_en[l[0]][1] += int(l[2])

main_dict = freq_dict_pl
divider_dict = freq_dict_en	 
if sys.argv[1] == "en-pl":
	main_dict = freq_dict_en
	divider_dict = freq_dict_pl	
		
factors = {} 
wspolne = 0
inne = 0
for word, values in main_dict.iteritems():
	if values[1] < 5:
		continue
	if divider_dict.has_key(word):
		try:
			wspolne += 1
			divider_freq = divider_dict[word][0]
		except:
			continue	
	else:
		divider_dict[word] = [0, 0]
		divider_freq = 0	
		inne += 1
	try:	
		factors[word] = int(values[0])/(divider_freq + K)
	except:
		continue
out = open(OUT_FILE, 'w+')			
for w in sorted(factors, key=factors.get, reverse=False):
	print factors[w], w, main_dict[w][0], divider_dict[w][0]
	out.write("%f %s %i %i\n" % (factors[w], w, main_dict[w][0], divider_dict[w][0]))
