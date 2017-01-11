import abc

import github.Repository as GithubRepository
from github.GithubException import GithubException

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

    @property
    def feature(self):
        if not self.features:
            raise IndexError()
        if len(self.features) > 1:
            raise NoUniqueFeatureExists()
        return self.features[0]

    @feature.setter
    def feature(self, value: Feature):
        if len(self.features) > 1:
            raise NoUniqueFeatureExists()
        if not self.features:
            self.features.append(value)
        else:
            self.features[0] = value

    def extract(self, api_repo: GithubRepository = None) -> [Feature]:
        self._api_repo = api_repo
        try:
            self._extract()
        except GithubException:
            return self.features
        return self.features

    @abc.abstractmethod
    def _init_features(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def _extract(self):
        raise NotImplementedError('Main class should not be called for feature extraction!')


class NoUniqueFeatureExists(Exception):
    pass


class NoRepositoryAvailable(Exception):
    pass
