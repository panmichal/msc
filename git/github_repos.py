from github_data import github_data
import csv

Github = github_data()

Github = github_data()
Github.load_config("config.json")
pl_repos = {}
pl_repos_file = open('repos_pl.txt', 'a')
pl_repos_writer = csv.writer(pl_repos_file )
uk_repos_file = open('repos_uk.txt', 'a')
uk_repos_writer = csv.writer(uk_repos_file)
uk_repos = {}
pl_users_lines = open("users_pl.txt").readlines()
pl_users = []
uk_users_lines = open("users_uk.txt").readlines()
uk_users = []
existing_repos = []
last_user_id = 34537
for pl_user_line in pl_users_lines:
	line = pl_user_line.split(',')
	if int(line[2]) > last_user_id:
		pl_users.append({"username":line[0], "email":line[1], "id":line[2]})
	else:
		print "SKIPPED " + 	line[2]
			
for uk_user_line in uk_users_lines:
	line = uk_user_line.split(',')
	if int(line[2]) > last_user_id:
		uk_users.append({"username":line[0], "email":line[1], "id":line[2]})
	else:
		print "SKIPPED " + 	line[2]

for user in pl_users:
	repos = Github.get_user_repos(user['username'])
	print user['email'] + ": " + str(len(repos))
	pl_repos[user['username']] = repos
for user in uk_users:
	repos = Github.get_user_repos(user['username'])
	print user['email'] + ": " + str(len(repos))
	uk_repos[user['username']] = repos
	
del pl_users[0:len(pl_users)]
del uk_users[0:len(uk_users)]	
for user, repos in pl_repos.iteritems():
	for repo in repos:
		pl_repos_writer.writerow([repo['name'], repo['owner']['login'], user])		
for user, repos in uk_repos.iteritems():
	for repo in repos:
		uk_repos_writer.writerow([repo['name'], repo['owner']['login'], user])	
