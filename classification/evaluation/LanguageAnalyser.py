import string
from collections import OrderedDict

from github.GithubException import GithubException

from classification.GithubAuthentification import GithubAuthentification
from classification.InputParser import InputParser
from classification.models import Repository


class LanguageAnalyser:
    def analyse(self, text):
        urls, labels = InputParser(text, train=True).parse()

        github = GithubAuthentification()

        languages = []
        for url in urls:
            try:
                languages.append(github.get_repo(url[19:]).get_languages())
            except GithubException:
                pass

        categories = [c.name for c in Repository.CATEGORIES]
        language_frequency = {}

        for category in categories:
            language_frequency[category] = {}

        for language_dict, label in zip(languages, labels):
            label = label.rstrip()
            for language, size in language_dict.items():
                if language not in language_frequency[label]:
                    language_frequency[label][language] = 0
                language_frequency[label][language] += size

        result_text = ''

        for category in language_frequency:
            result_text += '{}: '.format(category)
            category_frequency = language_frequency[category]
            ordered = OrderedDict(sorted(category_frequency.items(), key=lambda t: t[1], reverse=True))
            for language, size in ordered.items():
                if size > 0:
                    result_text += '({}, {}) '.format(language, size)
            result_text += '\n'

        return result_text
