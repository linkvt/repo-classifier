import string

from github import Repository as GithubRepository

from classification.evaluation.BaseAnalyser import BaseAnalyser


class DescriptionAnalyser(BaseAnalyser):
    def __init__(self):
        super().__init__()
        self._stop_words = ['the', 'in', 'of', 'this', 'that', 'for', 'and', 'at', 'on', 'with', 'a', 'an', 'to', 'as',
                            'with', 'is', '-']

    def _get_data_entry(self, repo: GithubRepository):
        return repo.description

    def _extract_information(self, frequencies, entry, label):
        desc = entry.translate(string.punctuation).lower() if entry else ''
        words = desc.split()

        for word in words:
            if word in self._stop_words:
                continue
            frequencies[label][word] += 1
