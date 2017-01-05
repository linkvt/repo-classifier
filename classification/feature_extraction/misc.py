"""Contains extractors that belong to no specific category but can be used in multiple categories."""
from github import GithubException

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature


class DescriptionKeyWordExtractor(FeatureExtractor):
    # TODO: Add more keywords
    keywords = ['homework', 'lecture', 'course', 'framework', 'assignment', 'application', 'api', 'webapp', 'icons',
                'data', 'list', 'fonts', 'materials', 'introduction', 'github', 'website', 'site', 'page', 'assignment',
                'group', 'official', 'documentation', 'document', 'dokument', 'policy']

    def _init_features(self):
        self.features = [Feature(name='Contains keyword "' + keyword + '"') for keyword in self.keywords]

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
        self.features = [Feature(name='Contains file "' + filename + '"') for filename in self.filenames]

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
