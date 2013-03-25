from github_data import github_data
import csv

Github = github_data()
Github.load_config("config.json")
pl_users = []
pl_file = open('users_pl.txt', 'a')
pl_writer = csv.writer(pl_file)
uk_file = open('users_uk.txt', 'a')
uk_writer = csv.writer(uk_file)
uk_users = []
last_user = 34537
SURNAMES_FILE = "../nazwiska_popularne.txt"
NAMES_FILE = "../imiona.txt"
surnames = [line.split()[1].lower() for line in open(SURNAMES_FILE).readlines() if len(line.split()[1]) > 3]
names = [line.strip() for line in open(NAMES_FILE).readlines()]

def create_patterns():
	search_patterns = []
	for surname in surnames:
		for name in names:
			search_patterns.append("%s %s" % (name.lower(), surname.lower()))
	return search_patterns		

def is_user_polish(user_data, patterns):
	if user_data['email'].endswith('.pl'):
		return True
	if 'name' in user_data and user_data['name'] != None:	
		for pattern in patterns:
			if user_data['name'].lower().encode('utf-8','ignore').find(pattern) != -1:
				return True			
	return False			
	
while (True):
	print "LAST USER: " + str(last_user)
	users = Github.get_users(last_user)
	name_patterns = create_patterns()
	for user in users:
		print(".")
		try:
			last_user = user['id']
		except:
			print user
			continue	
		user_data = Github.get_user(user['login'])
		if 'email' in user_data and user_data['email'] != None:
			if is_user_polish(user_data, name_patterns):
				pl_users.append({user['login'] : user_data['email']})
				print "PL: " + user_data['email'] + " Name: " + user_data['name']
				pl_writer.writerow([user['login'], user_data['email'], user['id']])
			elif user_data['email'].endswith('.uk'):
				uk_users.append({user['login'] : user_data['email']})
				print "UK: " + user_data['email']
				uk_writer.writerow([user['login'], user_data['email'], user['id']])	
