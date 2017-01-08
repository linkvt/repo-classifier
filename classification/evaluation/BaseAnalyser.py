from abc import ABC, abstractmethod
from collections import OrderedDict
from collections import defaultdict
from multiprocessing.pool import ThreadPool
from typing import DefaultDict, Any

from github import GithubException
from github import Repository as GithubRepository

from classification.GithubAuthentification import GithubAuthentification
from classification.InputParser import InputParser


class BaseAnalyser(ABC):
    def analyse(self, text):
        urls, labels = InputParser(text, train=True).parse()

        with ThreadPool(10) as pool:
            data = pool.map(self._get_data_entry_from_url, urls, 1)

        frequencies = defaultdict(lambda: defaultdict(int))
        for entry, label in zip(data, labels):
            if not entry:
                continue
            label = label.rstrip()
            self._extract_information(frequencies, entry, label)

        return self._pretty_print(frequencies)

    def _get_data_entry_from_url(self, url: str):
        github = GithubAuthentification()
        repo = github.get_repo(url[19:])
        try:
            return self._get_data_entry(repo)
        except GithubException:
            pass

    @abstractmethod
    def _get_data_entry(self, repo: GithubRepository):
        pass

    @abstractmethod
    def _extract_information(self, frequencies, entry, label):
        pass

    def _pretty_print(self, frequencies: DefaultDict[Any, DefaultDict[Any, int]]) -> str:
        result_text = ''

        for category in frequencies:
            result_text += '{}: '.format(category)
            category_frequency = frequencies[category]
            ordered = OrderedDict(sorted(category_frequency.items(), key=lambda t: t[1], reverse=True))
            for word, frequency in ordered.items():
                if frequency > 1:
                    result_text += '({}, {}) '.format(word, frequency)
            result_text += '\n'

        return result_text
