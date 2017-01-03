import string
from collections import OrderedDict

from classification.GithubAuthentification import GithubAuthentification
from classification.InputParser import InputParser
from classification.models import Repository


class DescriptionAnalyser:
    def __init__(self, text):
        self.text = text

    def analyse(self):
        urls, labels = InputParser(self.text, train=True).parse()

        github = GithubAuthentification()

        descriptions = [github.get_repo(url[19:]).description for url in urls]

        categories = [c.name for c in Repository.CATEGORIES]
        stopwords = ['the', 'in', 'of', 'this', 'that', 'for', 'and', 'at', 'on', 'with', 'a', 'an', 'to', 'as', 'with',
                     'is', '-']

        word_frequency = {}

        for category in categories:
            word_frequency[category] = {}

        for desc, label in zip(descriptions, labels):
            label = label.rstrip()
            desc = desc.translate(string.punctuation).lower() if desc else ''
            words = desc.split()

            for word in words:
                if word in stopwords:
                    continue
                if word not in word_frequency[label]:
                    word_frequency[label][word] = 0
                word_frequency[label][word] += 1

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
