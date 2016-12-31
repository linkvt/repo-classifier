import abc

from github.Repository import Repository

from classification.GithubAuthentification import GithubAuthentification
from classification.models import Feature


class FeatureExtractor:
    """
    Base class for all feature extractors.
    """

    def __init__(self, repo: Repository):
        self._api_repo = None
        self.repo = repo
        self.features = []

    @property
    def api_repo(self):
        """
        :return: a lazily initialized Github API repository
        """
        if not self._api_repo:
            self._api_repo = GithubAuthentification().get_repo(self.repo.identifier)
        return self._api_repo

    @abc.abstractmethod
    def extract_features(self) -> [Feature]:
        """
        :return: Feature
        """
        raise NotImplementedError('Main class should not be called for feature extraction!')
