from itertools import chain

import multiprocessing
from typing import List, Type

from github.Repository import Repository

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature
from classification.feature_extraction import common
from classification.feature_extraction.CachedFeatureExtractor import CachedFeatureExtractor

FEATURE_EXTRACTORS = [
    common.BranchExtractor,
    common.CommitNumberExtractor,
    common.ContributorsExtractor,
    common.ForkExtractor,
    common.StarExtractor,
    common.TotalFilesExtractor,
]


class FeatureExtractionPipeline:
    def __init__(self, repo: Repository):
        self._repo = repo

    def extract_features(self) -> [Feature]:
        pool = multiprocessing.Pool(len(FEATURE_EXTRACTORS))
        feature_lists = pool.map(self._extract_from_single_extractor, FEATURE_EXTRACTORS)
        return list(chain.from_iterable(feature_lists))

    def _extract_from_single_extractor(self, extractor: Type[FeatureExtractor]) -> List[Feature]:
        cached_extractor = CachedFeatureExtractor(extractor(self._repo))
        return cached_extractor.extract_features()
