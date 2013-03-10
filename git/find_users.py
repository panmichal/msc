import requests

users = requests.get('https://api.github.com/users/richcollins', auth=('github_user', 'github_password'))
