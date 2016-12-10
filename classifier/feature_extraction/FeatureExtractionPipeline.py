from github.Repository import Repository

from classifier.Feature import Feature
from classifier.feature_extraction.language.LanguageDEVFeatureExtractor import LanguageDEVFeatureExtractor

FEATURE_ORDER = [
    LanguageDEVFeatureExtractor
]


class FeatureExtractionPipeline:
    def __init__(self, repo: Repository):
        self.__repo = repo

    def extract_features(self):
        return [Feature('Test feature with forks', self.__repo.forks)] + [feature(self.__repo).extract_feature() for
                                                                          feature in FEATURE_ORDER]
