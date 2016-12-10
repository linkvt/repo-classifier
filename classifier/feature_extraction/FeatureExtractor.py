from github.Repository import Repository

from classifier import Feature


class FeatureExtractor:
    """
    Base class for all feature extractors.
    """
    def __init__(self, repo: Repository):
        self.repo = repo

    def extract_feature(self) -> Feature:
        """
        :return: Feature
        """
        raise NotImplementedError('Main class should not be called for feature extraction!')
