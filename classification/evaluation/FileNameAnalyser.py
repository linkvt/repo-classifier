from github import Repository as GithubRepository

from classification.evaluation.BaseAnalyser import BaseAnalyser


class FileNameAnalyser(BaseAnalyser):
    def __init__(self):
        super().__init__()
        self._stop_files = ['.gitignore', 'README.md']

    def _get_data_entry(self, repo: GithubRepository):
        return repo.get_dir_contents('')

    def _extract_information(self, frequencies, entry, label):
        for file in entry:
            if file.name in self._stop_files:
                continue
            frequencies[label][file.name] += 1
