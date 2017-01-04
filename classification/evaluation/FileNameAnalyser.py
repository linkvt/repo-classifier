import string
from collections import OrderedDict

from github.GithubException import GithubException

from classification.GithubAuthentification import GithubAuthentification
from classification.InputParser import InputParser
from classification.models import Repository


class FileNameAnalyser:
    def analyse(self, text):
        urls, labels = InputParser(text, train=True).parse()

        github = GithubAuthentification()

        files = []
        for url in urls:
            try:
                files.append(github.get_repo(url[19:]).get_dir_contents(''))
            except GithubException:
                pass

        categories = [c.name for c in Repository.CATEGORIES]
        stop_files = ['.gitignore', 'README.md']

        word_frequency = {}

        for category in categories:
            word_frequency[category] = {}

        for root, label in zip(files, labels):
            label = label.rstrip()

            for file in root:
                if file.name in stop_files:
                    continue
                if file.name and file.name not in word_frequency[label]:
                    word_frequency[label][file.name] = 0
                word_frequency[label][file.name] += 1

        result_text = ''

        for category in word_frequency:
            result_text += '{}: '.format(category)
            category_frequency = word_frequency[category]
            ordered = OrderedDict(sorted(category_frequency.items(), key=lambda t: t[1], reverse=True))
            for word, frequency in ordered.items():
                if frequency > 1:
                    result_text += '({}, {}) '.format(word, frequency)
            result_text += '\n'

        return result_text
