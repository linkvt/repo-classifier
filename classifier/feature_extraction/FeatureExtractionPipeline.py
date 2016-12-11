from github.Repository import Repository

from classifier.Feature import Feature
from classifier.feature_extraction.language.LanguageDEVFeatureExtractor import LanguageDEVFeatureExtractor

FEATURE_ORDER = [
    LanguageDEVFeatureExtractor
]


class FeatureExtractionPipeline:
    def __init__(self, repo: Repository):
        self._repo = repo

    def extract_features(self):
        return [Feature('Test feature with forks', self._repo.forks)] + [feature(self._repo).extract_feature() for
                                                                         feature in FEATURE_ORDER]
