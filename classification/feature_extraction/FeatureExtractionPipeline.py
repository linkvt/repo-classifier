from itertools import chain

from github.Repository import Repository

from classification.Feature import Feature
from classification.feature_extraction.FeatureCategory import FeatureCategory
from classification.feature_extraction.MainCategory import MainCategory

CATEGORIES = [
    MainCategory
]


class FeatureExtractionPipeline:
    def __init__(self, repo: Repository):
        self._repo = repo

    def extract_features(self) -> [Feature]:
        return list(chain.from_iterable((category.extract() for category in self.extract_features_in_categories())))

    def extract_features_in_categories(self) -> [FeatureCategory]:
        return [category(self._repo) for category in CATEGORIES]
