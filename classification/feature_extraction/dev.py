"""Contains extractors that are used for the DEV category."""

from github import GithubException

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature


class HasBuildFileExtractor(FeatureExtractor):
    # TODO: Add more build files
    build_files = ['build.gradle', 'composer.json', 'makefile' 'package.json', 'pom.xml']

    def _init_features(self):
        self.features = [Feature('Has build file')]

    def _extract(self):
        try:
            files = self.api_repo.get_dir_contents('')
        except GithubException:
            files = []

        self.features[0].value = 0
        for file in files:
            if file.name and file.name.lower() in self.build_files:
                self.features[0].value = 1
