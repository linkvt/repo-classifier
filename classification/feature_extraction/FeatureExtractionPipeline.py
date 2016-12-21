from itertools import chain

from github.Repository import Repository

from classification.Feature import Feature
from classification.feature_extraction import common

FEATURE_EXTRACTORS = [
    common.BranchExtractor,
    common.CommitNumberExtractor,
    common.ContributorsExtractor,
    common.ForkExtractor,
    common.StarExtractor,
]


class FeatureExtractionPipeline:
    def __init__(self, repo: Repository):
        self._repo = repo

    def extract_features(self) -> [Feature]:
        return list(chain.from_iterable((extractor(self._repo).extract_features() for extractor in FEATURE_EXTRACTORS)))
