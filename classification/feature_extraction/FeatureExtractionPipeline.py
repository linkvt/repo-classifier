import itertools
from itertools import chain
from multiprocessing.pool import ThreadPool
from typing import List, Type

from classification.feature_extraction import common, misc, dev, web
from classification.feature_extraction.CachedFeatureExtractor import CachedFeatureExtractor
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
    dev.HasBuildFileExtractor,
    dev.LanguageDEVExtractor,
    misc.DescriptionKeyWordExtractor,
    misc.FileNameExtractor,
    web.LanguageWEBExtractor,
]


def extract_from_single_extractor(data: (Type[FeatureExtractor], Repository)) -> List[Feature]:
    cached_extractor = CachedFeatureExtractor(data[0](data[1]))
    return cached_extractor.extract()


class FeatureExtractionPipeline:
    def __init__(self):
        self._pool = ThreadPool(len(FEATURE_EXTRACTORS))

    def extract_features(self, repo: Repository) -> [Feature]:
        data = zip(FEATURE_EXTRACTORS, itertools.repeat(repo))
        feature_lists = self._pool.imap(extract_from_single_extractor, data, chunksize=5)
        return list(chain.from_iterable(feature_lists))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Clean up spawned child processes
        :return:
        """
        self._pool.terminate()
