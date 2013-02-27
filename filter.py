import os
import sys
import mmap

SURNAMES_FILE = "nazwiska_popularne.txt"
NAMES_FILE = "imiona.txt"
FILTERED_INDEX = "filtered_texts.txt"

def get_search_patterns():
	search_patterns = []
	surnames = [line.split()[1].lower() for line in open(SURNAMES_FILE).readlines() if len(line.split()[1]) > 3]
	names = [line.strip() for line in open(NAMES_FILE).readlines()]
	for surname in surnames:
		for name in names:
			search_patterns.append("%s %s" % (name, surname))
			search_patterns.append("%s. %s" % (name[0], surname))
	return search_patterns
		
counter = 0
found = 0
search_patterns = get_search_patterns()
filtered_index = open(FILTERED_INDEX, 'a+')
already_filtered = [path.split()[0] for path in filtered_index.readlines()]
for root, dirs, files in os.walk(sys.argv[1]):
	for f in files:
		relative_path = root + "/" + f
		if relative_path in already_filtered:
			print "[SKIPPING] %s" % (relative_path)
			continue
		counter += 1
		txt = open(relative_path)
		try:
			#s = mmap.mmap(txt.fileno(), 512, access=mmap.ACCESS_READ)
			s = txt.read(512)
		except:
			print "[ERROR]"	
			continue
		is_polish = 0
		for pattern in search_patterns:
			if s.find(pattern) != -1:
				print "[FOUND] " + pattern
				is_polish = 1
				found += 1
				break		
		filtered_index.write("%s %i\n" % (relative_path, is_polish))			
		print "[%s/%s] %s" % (found, counter, relative_path)					
print "Finished: %s/%s" %(found, counter)
