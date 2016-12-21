from itertools import chain
from github.Repository import Repository

from classification.Feature import Feature
from classification.feature_extraction.CommonFeatureExtractors import ContributorsExtractor, BranchExtractor, \
    ForkExtractor, StarExtractor, CommitNumberExtractor

FEATURE_EXTRACTORS = [
    BranchExtractor,
    CommitNumberExtractor,
    ContributorsExtractor,
    ForkExtractor,
    StarExtractor,
]


class FeatureExtractionPipeline:
    def __init__(self, repo: Repository):
        self._repo = repo

    def extract_features(self) -> [Feature]:
		return list(chain.from_iterable(
            (extractor(self._repo).extract_features() for extractor in FEATURE_EXTRACTORS)))
