import itertools

from classifier import Feature
from classifier.feature_extraction.FeatureExtractor import FeatureExtractor


class FeatureCategory:
    """
    Each category is a representation for a own weightable feature set.
    This can be for example be used for own trees.
    """

    def __init__(self, repo):
        self.repo = repo
        self.categories = self._get_categories()
        self.weight = self._get_weight()
        self.features = list(itertools.chain.from_iterable(
            (extractor.extract_features() for extractor in self._get_feature_extractors())))
        self.validate()

    def _get_weight(self) -> float:
        """
        Value between 0 and 1
        :return:
        """
        return 1

    def extract(self) -> [Feature]:
        if self.categories:
            return list(itertools.chain.from_iterable((category.extract() for category in self.categories)))
        return self.features

    def validate(self):
        if self.categories and self.features:
            raise AssertionError('Categories and features are both filled.')
        if not self.categories and not self.features:
            raise AssertionError('Categories and features are both empty')


    def _get_categories(self):
        return []

    def _get_feature_extractors(self) -> [FeatureExtractor]:
        return []
