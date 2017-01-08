import os

from github import Repository as GithubRepository

from classification.evaluation.BaseAnalyser import BaseAnalyser


class FileExtensionAnalyser(BaseAnalyser):
    def _get_data_entry(self, repo: GithubRepository):
        git_tree = repo.get_git_tree(repo.default_branch, recursive=True)
        items = git_tree.tree if git_tree else []
        files = [item for item in items if item.type == 'blob']
        extensions = [os.path.splitext(file.path)[1] for file in files]
        return extensions

    def _extract_information(self, frequencies, entry, label):
        for extension in entry:
            frequencies[label][extension] += 1
