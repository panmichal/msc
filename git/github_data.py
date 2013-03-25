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
		
	def get_user_repos(self, username):
		repos = requests.get('https://api.github.com/users/' + username + '/repos', auth=(self.username, self.password), params = {"type":"public"}) 
		return repos.json
		
	def get_commits_from_author(self, repo_name, repo_owner, author):
		commits = requests.get('https://api.github.com/repos/' + repo_owner + "/" + repo_name +'/commits', auth=(self.username, self.password))	
		return commits.json
