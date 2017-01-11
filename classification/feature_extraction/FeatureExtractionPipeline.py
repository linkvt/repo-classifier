import logging
import typing
from multiprocessing.pool import ThreadPool

import github.Repository as GithubRepository

from classification.GithubAuthentification import GithubAuthentification
from classification.feature_extraction import common, misc, data, dev, docs, web
from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature, Repository

FEATURE_EXTRACTORS = [
    common.ActiveTimeExtractor,
    common.BranchExtractor,
    common.CommitNumberExtractor,
    common.ContributorsExtractor,
    common.ForkExtractor,
    common.HasDownloadsExtractor,
    common.HasIssuesExtractor,
    common.HasPagesExtractor,
    common.HasWikiExtractor,
    common.IsForkExtractor,
    common.OpenIssueExtractor,
    common.SizeExtractor,
    common.StarExtractor,
    common.TotalFilesExtractor,
    common.WatchersExtractor,
    data.DATAFileExtensionExtractor,
    dev.HasBuildFileExtractor,
    dev.LanguageDEVExtractor,
    docs.DOCSFileExtensionExtractor,
    misc.DescriptionKeyWordExtractor,
    misc.FileNameExtractor,
    web.LanguageWEBExtractor,
    web.DescriptionContainsURLExtractor,
]

logger = logging.getLogger(__name__)


class FeatureExtractionPipeline:
    cache_features = True

    def __init__(self):
        self._github_authentication = GithubAuthentification()

    def extract_features(self, repos: [Repository]) -> [[Feature]]:
        with ThreadPool(4) as pool:
            feature_lists = pool.map(self._extract_for_single_repo, repos, 2)
            return feature_lists

    def _extract_for_single_repo(self, repo: Repository) -> [Feature]:
        api_repo = self._create_api_repo(repo)
        extractors = [extractor(repo) for extractor in FEATURE_EXTRACTORS]
        features = []

        for extractor in extractors:
            extracted_features = self._extract_for_single_repo_single_extractor(extractor, repo, api_repo)
            features.extend(extracted_features)
        logger.info('Features of %s: %s', repo.identifier, features)

        return features

    def _create_api_repo(self, repo: Repository) -> GithubRepository:
        return self._github_authentication.get_repo(repo.identifier)

    def _extract_for_single_repo_single_extractor(self,
                                                  extractor: FeatureExtractor,
                                                  repo: Repository,
                                                  api_repo: GithubRepository) -> [Feature]:
        cached_features = []
        for feature in extractor.features:
            cached_feature = self._get_cached(repo, feature)
            if self.cache_features and cached_feature:
                cached_features.append(cached_feature)
            else:
                updated_features = extractor.extract(api_repo)
                for updated_feature in updated_features:
                    self._update_cached(repo, updated_feature)
                return updated_features
        return cached_features

    def _get_cached(self, repo: Repository, feature: Feature) -> typing.Union[Feature, None]:
        try:
            feature = Feature.objects.get(repository=repo, name=feature.name)
            return feature
        except Feature.DoesNotExist:
            return None

    def _update_cached(self, repo: Repository, feature: Feature):
        repo.feature_set.update_or_create(name=feature.name, defaults={'value': feature.value})
