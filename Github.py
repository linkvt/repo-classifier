import configparser

from github import Github

config = configparser.ConfigParser()
config.read("github.conf")

fileUsername = config.get("DEFAULT", "username")
filePassword = config.get("DEFAULT", "password")
fileToken = config.get("DEFAULT", "token")

if not fileUsername and not fileToken:
    print("Username and Token is not filled in github.conf file. Please input login data.")
    raise LookupError("github.conf is not properly filled.")

githubApi = None

if fileToken:
    githubApi = Github(fileToken)
else:
    githubApi = Github(fileUsername, filePassword)

for repo in githubApi.get_user().get_repos():
    print(repo.name)
