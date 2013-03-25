from github_data import github_data
import csv

Github = github_data()

Github = github_data()
Github.load_config("config.json")
pl_comments = {}
pl_comments_file = open('comments_pl.txt', 'a')
pl_comments_writer = csv.writer(pl_comments_file)
uk_comments_file = open('comments_uk.txt', 'a')
uk_comments_writer = csv.writer(uk_comments_file)
uk_comments = {}

pl_repos_lines = open("repos_pl.txt").readlines()
pl_repos = []
uk_repos_lines = open("repos_uk.txt").readlines()
uk_repos = []

last_username_pl = "ComputerDruid"
last_username_uk = "edendevelopment"

add_repo = False
for pl_repos_line in pl_repos_lines:
	line = pl_repos_line.split(',')
	if line[1] == last_username_pl:
		add_repo = True
	if add_repo == True:
		pl_repos.append({"name":line[0], "owner":line[1], "username":line[2]})
	else:
		print "SKIP: %s - %s" % (line[0], line[2])	
	
add_repo = False	
for uk_repos_line in uk_repos_lines:
	line = uk_repos_line.split(',')
	if line[1] == last_username_uk:
		add_repo = True
	if add_repo == True:	
		uk_repos.append({"name":line[0], "owner":line[1], "username":line[2]})
	else:
		print "SKIP: %s - %s" % (line[0], line[2])	
	
for repo in pl_repos:
	commits = Github.get_commits_from_author(repo['name'], repo['owner'], repo['username'])
	print "Repo: %s Autor: %s Commits: %s" % (repo['name'], repo['username'], str(len(commits)))
	for commit in commits:
		try:
			message = commit['commit']['message'].encode('utf-8','ignore')
			pl_comments_writer.writerow([message])
			print commit['commit']['message']
		except:
			print "error"
		
for repo in uk_repos:
	commits = Github.get_commits_from_author(repo['name'], repo['owner'], repo['username'])
	print "Repo: %s Autor: %s Commits: %s" % (repo['name'], repo['username'], str(len(commits)))
	for commit in commits:
		try:
			message = commit['commit']['message'].encode('utf-8','ignore')
			uk_comments_writer.writerow([message])
		except:
			print "error"	
		#print commit['commit']['message']		
		
