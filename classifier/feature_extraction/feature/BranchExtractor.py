from classifier.Feature import Feature
from classifier.feature_extraction.FeatureExtractor import FeatureExtractor


class BranchExtractor(FeatureExtractor):
    def extract_features(self) -> [Feature]:
        branches = self._repo.get_branches()
        num = len([branch for branch in branches])
        return [Feature('Number of branches', num)]
