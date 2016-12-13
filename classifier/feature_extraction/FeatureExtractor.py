import abc

from github.Repository import Repository

from classifier import Feature


class FeatureExtractor:
    """
    Base class for all feature extractors.
    """

    def __init__(self, repo: Repository):
        self._repo = repo

    @abc.abstractmethod
    def extract_features(self) -> [Feature]:
        """
        :return: Feature
        """
        raise NotImplementedError('Main class should not be called for feature extraction!')
