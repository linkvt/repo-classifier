from classification.Feature import Feature

from classification.feature_extraction.FeatureExtractor import FeatureExtractor


class StarExtractor(FeatureExtractor):
    def extract_features(self) -> [Feature]:
        return [Feature('Number of stars', self._repo.stargazers_count)]
