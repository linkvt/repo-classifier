from classification.Feature import Feature

from classification.feature_extraction.FeatureExtractor import FeatureExtractor


class ForkExtractor(FeatureExtractor):
    def extract_features(self) -> [Feature]:
        return [Feature('Test feature with forks', self._repo.forks)]
