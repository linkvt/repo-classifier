from classifier.Feature import Feature
from classifier.feature_extraction.language.LanguageFeatureExtractor import LanguageFeatureExtractor

FEATURE_ORDER = [
    LanguageFeatureExtractor
]


class FeatureExtractionPipeline:
    def __init__(self, repo):
        self.__repo = repo

    def extract_features(self):
        return [Feature('Test feature with forks', self.__repo.forks)] + [feature(self.__repo).extract_feature() for
                                                                          feature in FEATURE_ORDER]
