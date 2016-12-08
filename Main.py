import argparse

from GithubAuthentification import GithubAuthentication
from InputParser import InputParser

parser = argparse.ArgumentParser(description='Test')
parser.add_argument('--file', dest="filepath", help='The file location of the input file', nargs='?', required=True,
                    metavar='FILE')

args = parser.parse_args()

input_parser = InputParser(args.filepath)
splitted_urls = input_parser.parse()
github_connection = GithubAuthentication()

for url in splitted_urls:
    current_repo = github_connection.get_repo(url)
    print(current_repo.name)
    # TODO feature pipeline -> classifier pipeline -> output
