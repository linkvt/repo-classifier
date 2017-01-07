import configparser
import logging

from github import Github

logger = logging.getLogger(__name__)


class GithubAuthentification:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("github.conf")

        fileUsername = config.get("DEFAULT", "username")
        filePassword = config.get("DEFAULT", "password")
        fileToken = config.get("DEFAULT", "token")

        if not fileUsername and not fileToken:
            logger.error("Username and Token is not filled in github.conf file. Please input login data.")
            raise LookupError("github.conf is not properly filled.")

        if fileToken:
            self.api = Github(fileToken)
        else:
            self.api = Github(fileUsername, filePassword)

    def get_repo(self, identifier):
        return self.api.get_repo(identifier)

    def get_repos(self, since):
        return self.api.get_repos(since)
