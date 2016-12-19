from classification.Feature import Feature

from classification.feature_extraction.FeatureExtractor import FeatureExtractor


class CommitNumberExtractor(FeatureExtractor):
    def extract_features(self) -> [Feature]:
        contributors = self._repo.get_contributors()
        total_commits_default_branch = sum(contributor.contributions for contributor in contributors)
        return [Feature('Number of commits: ', total_commits_default_branch)]
