"""Contains common extractors that are used for all categories."""
from github import GithubException
from github.GitTree import GitTree

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature


class ActiveTimeExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Active time in days')]

    def _extract(self):
        # updated_at doesn't tell when the last activity happened: http://stackoverflow.com/a/15922637
        last_commit_date = self.api_repo.pushed_at
        initial_creation_date = self.api_repo.parent.created_at if self.api_repo.fork else self.api_repo.created_at
        active_time = last_commit_date - initial_creation_date
        self.features[0].value = active_time.days


class BranchExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Number of branches')]

    def _extract(self):
        branches = self.api_repo.get_branches()
        num = len([branch for branch in branches])
        self.features[0].value = num


class CommitNumberExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Number of commits')]

    def _extract(self):
        contributors = self.api_repo.get_contributors()
        total_commits_default_branch = sum(contributor.contributions for contributor in contributors)
        self.features[0].value = total_commits_default_branch


class ContributorsExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Number of contributors')]

    def _extract(self):
        contributors = self.api_repo.get_contributors()
        num = len([c for c in contributors])
        self.features[0].value = num


class ForkExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Number of forks')]

    def _extract(self):
        self.features[0].value = self.api_repo.forks


class HasDownloadsExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Has downloads')]

    def _extract(self):
        self.features[0].value = 1 if self.api_repo.has_downloads else 0


class HasIssuesExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Has issues')]

    def _extract(self):
        self.features[0].value = 1 if self.api_repo.has_issues else 0


class HasPagesExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Has pages')]

    def _extract(self):
        used_to_load_raw_data = self.api_repo.has_issues
        self.features[0].value = 1 if self.api_repo._rawData.get('has_pages') else 0


class HasWikiExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Has wiki')]

    def _extract(self):
        self.features[0].value = 1 if self.api_repo.has_wiki else 0


class IsForkExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Is a fork')]

    def _extract(self):
        self.features[0].value = 1 if self.api_repo.fork else 0


class OpenIssueExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Number of open issues')]

    def _extract(self):
        self.features[0].value = self.api_repo.open_issues_count


class SizeExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Size of repo')]

    def _extract(self):
        self.features[0].value = self.api_repo.size


class StarExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Number of stars')]

    def _extract(self):
        self.features[0].value = self.api_repo.stargazers_count


class TotalFilesExtractor(FeatureExtractor):
    """
    Extractor for returning the total number of files for the default branch of the repository.
    """

    def _init_features(self):
        self.features = [Feature(name='Number of files')]

    def _extract(self):
        # Boolean flag -> recursive call for contents
        try:
            total_num_files = self._get_num_files(self.api_repo.get_git_tree(self.api_repo.default_branch, True))
        except GithubException:
            total_num_files = 0
        self.features[0].value = total_num_files

    def _get_num_files(self, tree: GitTree) -> int:
        num_files = 0
        for item in tree.tree:
            if item.type == 'blob':
                num_files += 1
                # Because of recursive call ignore dirs seems to be working also with folders with 10000 files
        return num_files


class WatchersExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature(name='Number of watchers')]

    def _extract(self):
        self.features[0].value = self.api_repo.watchers_count
