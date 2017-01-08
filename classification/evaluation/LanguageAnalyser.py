from github import Repository as GithubRepository

from classification.evaluation.BaseAnalyser import BaseAnalyser


class LanguageAnalyser(BaseAnalyser):
    def _get_data_entry(self, repo: GithubRepository):
        return repo.get_languages()

    def _extract_information(self, frequencies, entry, label):
        for language, size in entry.items():
            frequencies[label][language] += size
