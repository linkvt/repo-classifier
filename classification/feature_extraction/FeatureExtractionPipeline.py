from github.Repository import Repository

from classification.Feature import Feature
from classification.feature_extraction.CommonFeatureExtractors import ContributorsExtractor, BranchExtractor, \
    ForkExtractor, StarExtractor, CommitNumberExtractor

FEATURE_EXTRACTORS = [
    BranchExtractor,
    ContributorsExtractor,
    ForkExtractor,
    StarExtractor,
    CommitNumberExtractor,
]


class FeatureExtractionPipeline:
    def __init__(self, repo: Repository):
        self._repo = repo

    def extract_features(self) -> [Feature]:
        return [extractor(self._repo).extract_features() for extractor in FEATURE_EXTRACTORS]
