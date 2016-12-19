from classification.Feature import Feature

from classification.feature_extraction.FeatureExtractor import FeatureExtractor


class ContributorsExtractor(FeatureExtractor):
    def extract_features(self) -> [Feature]:
        contributors = self._repo.get_contributors()
        num = len([c for c in contributors])
        return [Feature('Number of contributors', num)]