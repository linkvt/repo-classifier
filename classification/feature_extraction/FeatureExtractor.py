import abc

import github.Repository as GithubRepository

from classification.GithubAuthentification import GithubAuthentification
from classification.models import Feature, Repository


class FeatureExtractor:
    """
    Base class for all feature extractors.
    """

    def __init__(self, repo: Repository):
        self._api_repo = None
        self.repo = repo
        self.features = []
        self._init_features()

    @property
    def api_repo(self) -> GithubRepository:
        """
        :return: a lazily initialized Github API repository
        """
        if not self._api_repo:
            self._api_repo = GithubAuthentification().get_repo(self.repo.identifier)
        return self._api_repo

    def extract(self) -> [Feature]:
        self._extract()
        return self.features

    @abc.abstractmethod
    def _init_features(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def _extract(self):
        raise NotImplementedError('Main class should not be called for feature extraction!')
