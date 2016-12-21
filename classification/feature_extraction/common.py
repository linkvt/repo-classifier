from github import Repository
from github.GitTree import GitTree

from classification.Feature import Feature
from classification.feature_extraction.FeatureExtractor import FeatureExtractor


class BranchExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Number of branches')]

    def extract_features(self) -> [Feature]:
        branches = self.repo.get_branches()
        num = len([branch for branch in branches])
        self.features[0].value = num
        return self.features


class CommitNumberExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Number of commits')]

    def extract_features(self) -> [Feature]:
        contributors = self.repo.get_contributors()
        total_commits_default_branch = sum(contributor.contributions for contributor in contributors)
        self.features[0].value = total_commits_default_branch
        return self.features


class ContributorsExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Number of contributors')]

    def extract_features(self) -> [Feature]:
        contributors = self.repo.get_contributors()
        num = len([c for c in contributors])
        self.features[0].value = num
        return self.features


class ForkExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Number of forks')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.repo.forks
        return self.features


class HasDownloadsExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Has downloads')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = 1 if self.repo.has_downloads else 0
        return self.features


class HasIssuesExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Has issues')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = 1 if self.repo.has_issues else 0
        return self.features


class HasWikiExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Has wiki')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = 1 if self.repo.has_wiki else 0
        return self.features


class IsForkExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Is a fork')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = 1 if self.repo.fork else 0
        return self.features


class OpenIssueExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Number of open issues')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.repo.open_issues_count
        return self.features


class SizeExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Size of repo')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.repo.size
        return self.features


class StarExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Number of stars')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.repo.stargazers_count
        return self.features


class TotalFilesExtractor(FeatureExtractor):
    """
    Extractor for returning the total number of files for the default branch of the repository.
    TODO needs testing with num files > 1000 in one folder because the API limits the recursive call to 1000.
    TODO testing file sizes > 1mb
    """

    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Number of files')]

    def extract_features(self) -> [Feature]:
        # Not sure if master is always the best approach. Maybe it is better to request the latest commit and use the
        # SHA of it
        tree = self.repo.get_git_tree('master')
        assert isinstance(tree, GitTree), tree

        total_num_files = self._get_num_files(tree)
        self.features[0].value = total_num_files
        return self.features

    def _get_num_files(self, tree: GitTree) -> int:
        num_files = 0
        for item in tree.tree:
            if item.type == 'blob':
                num_files += 1
            else:
                # If not tree we have to request the new information -> cost intensive but no other way
                num_files += self._get_num_files(item)
        return num_files


class WatchersExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Number of watchers')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.repo.watchers_count
        return self.features
