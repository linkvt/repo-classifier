import multiprocessing
from itertools import chain
from typing import List, Type

import itertools

from classification.feature_extraction import common
from classification.feature_extraction.CachedFeatureExtractor import CachedFeatureExtractor
from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature, Repository

FEATURE_EXTRACTORS = [
    common.BranchExtractor,
    common.CommitNumberExtractor,
    common.ContributorsExtractor,
    common.ForkExtractor,
    common.StarExtractor,
    common.TotalFilesExtractor,
]


def extract_from_single_extractor(data: (Type[FeatureExtractor], Repository)) -> List[Feature]:
    cached_extractor = CachedFeatureExtractor(data[0](data[1]))
    return cached_extractor.extract_features()


class FeatureExtractionPipeline:
    def __init__(self):
        self._pool = multiprocessing.Pool(len(FEATURE_EXTRACTORS))

    def extract_features(self, repo: Repository) -> [Feature]:
        data = zip(FEATURE_EXTRACTORS, itertools.repeat(repo))
        feature_lists = self._pool.map(extract_from_single_extractor, data)
        return list(chain.from_iterable(feature_lists))
