"""Contains extractors that belong to no specific category but can be used in multiple categories."""
import abc
import os
import typing
from collections import defaultdict

from github import GithubException

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature


class DescriptionKeyWordExtractor(FeatureExtractor):
    # TODO: Add more keywords
    keywords = ['homework', 'lecture', 'course', 'framework', 'assignment', 'application', 'api', 'webapp', 'icons',
                'data', 'list', 'fonts', 'materials', 'introduction', 'github', 'website', 'site', 'page', 'assignment',
                'group', 'official', 'documentation', 'document', 'dokument', 'policy']

    def _init_features(self):
        self.features = [Feature.create('Contains keyword "' + keyword + '"') for keyword in self.keywords]

    def _extract(self):
        description = self.api_repo.description.lower() if self.api_repo.description else ''

        for keyword, feature in zip(self.keywords, self.features):
            if keyword in description:
                feature.value = 1
            else:
                feature.value = 0


class FileNameExtractor(FeatureExtractor):
    filenames = ['index.html', 'css', 'js', 'img', 'images', 'fonts', 'src']

    def _init_features(self):
        self.features = [Feature.create('Contains file "' + filename + '"') for filename in self.filenames]

    def _extract(self):
        repo_filenames = []
        try:
            repo_files = self.api_repo.get_dir_contents('')
            repo_filenames = [file.name for file in repo_files if file.name]
        except GithubException:
            pass
        for filename, feature in zip(self.filenames, self.features):
            if filename in repo_filenames:
                feature.value = 1
            else:
                feature.value = 0


class FileExtensionExtractor(FeatureExtractor):
    def _init_features(self):
        self._extension_to_count_feature = Feature.create('Share of {}-extensions by count'.format(self.category))
        self._extension_to_size_feature = Feature.create('Share of {}-extensions by size'.format(self.category))
        self.features = [self._extension_to_count_feature, self._extension_to_size_feature]

    def _extract(self):
        try:
            git_tree = self.api_repo.get_git_tree(self.api_repo.default_branch, recursive=True)
        except GithubException:
            git_tree = None
        items = git_tree.tree if git_tree else []
        files = [item for item in items if item.type == 'blob']

        extensions_to_count = defaultdict(int)
        extensions_to_size = defaultdict(int)
        for file in files:
            _, extension = os.path.splitext(file.path)
            extension = extension.lower()
            extensions_to_count[extension] += 1
            extensions_to_size[extension] += file.size

        total_count = sum(extensions_to_count.values())
        total_size = sum(extensions_to_size.values())

        relevant_count = sum(extensions_to_count[ext] for ext in self.extensions_to_check)
        relevant_size = sum(extensions_to_size[ext] for ext in self.extensions_to_check)

        self._extension_to_count_feature.value = relevant_count / total_count if total_count else 0
        self._extension_to_size_feature.value = relevant_size / total_size if total_size else 0

    @property
    @abc.abstractmethod
    def category(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def extensions_to_check(self) -> typing.Set[str]:
        raise NotImplementedError()
