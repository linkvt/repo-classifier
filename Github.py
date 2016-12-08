from github import Github
import configparser

config = configparser.ConfigParser()
config.read('github.conf')

fileUsername = config.get("DEFAULT", "username")
filePassword = config.get("DEFAULT", "password")
fileToken = config.get("DEFAULT", "token")

if not fileUsername:
        print("Username is not filled in github.conf file. Please input login data.")
        raise LookupError("github.conf is not properly filled.")

g = Github(fileUsername, filePassword)

for repo in g.get_user().get_repos():
    print(repo.name)
