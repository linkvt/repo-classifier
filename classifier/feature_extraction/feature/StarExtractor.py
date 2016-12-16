from classifier.Feature import Feature
from classifier.feature_extraction.FeatureExtractor import FeatureExtractor


class StarExtractor(FeatureExtractor):
    def extract_features(self) -> [Feature]:
        return [Feature('Number of stars', self._repo.stargazers_count)]
