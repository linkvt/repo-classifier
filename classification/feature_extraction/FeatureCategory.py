import abc
from itertools import chain

from classification import Feature
from classification.feature_extraction import FeatureExtractor


class FeatureCategory:
    """
    Each category is a representation for a own weightable feature set.
    This can be for example be used for own trees.
    """

    def __init__(self, repo):
        self.repo = repo
        self.features = list(chain.from_iterable(
            (extractor.extract_features() for extractor in self._get_feature_extractors())))

    def extract(self) -> [Feature]:
        return self.features

    @abc.abstractmethod
    def _get_feature_extractors(self) -> [FeatureExtractor]:
        raise AssertionError('Must be overridden')
