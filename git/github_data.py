import requests
import json
import csv
import sys

class github_data:
	def load_config(self, config_file):
		json_data=open(config_file)
		self.config = json.load(json_data)
		self.username = self.config["github_username"]
		self.password = self.config["github_password"]
		
	def get_users(self, last_id = 0):
		users = requests.get('https://api.github.com/users', auth=(self.username, self.password), params = {"since":last_id})
		return users.json
	def get_user(self, username):
		user = requests.get('https://api.github.com/users/' + username, auth=(self.username, self.password)) 
		return user.json

Github = github_data()
Github.load_config("config.json")
pl_users = []
pl_file = open('users_pl.txt', 'a')
pl_writer = csv.writer(pl_file)
uk_file = open('users_uk.txt', 'a')
uk_writer = csv.writer(uk_file)
uk_users = []
last_user = 14021
while (True):
	print "LAST USER: " + str(last_user)
	users = Github.get_users(last_user)
	for user in users:
		print(".")
		try:
			last_user = user['id']
		except:
			print user
			continue	
		user_data = Github.get_user(user['login'])
		if 'email' in user_data and user_data['email'] != None:
			if user_data['email'].endswith('.pl'):
				pl_users.append({user['login'] : user_data['email']})
				print "PL: " + user_data['email']
				pl_writer.writerow([user['login'], user_data['email'], user['id']])
			elif user_data['email'].endswith('.uk'):
				uk_users.append({user['login'] : user_data['email']})
				print "UK: " + user_data['email']
				uk_writer.writerow([user['login'], user_data['email'], user['id']])	
