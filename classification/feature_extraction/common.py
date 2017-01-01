from github import Repository
from github.GitTree import GitTree
from github.GithubException import GithubException

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature


class BranchExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Number of branches')]

    def extract_features(self) -> [Feature]:
        branches = self.api_repo.get_branches()
        num = len([branch for branch in branches])
        self.features[0].value = num
        return self.features


class CommitNumberExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Number of commits')]

    def extract_features(self) -> [Feature]:
        contributors = self.api_repo.get_contributors()
        total_commits_default_branch = sum(contributor.contributions for contributor in contributors)
        self.features[0].value = total_commits_default_branch
        return self.features


class ContributorsExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Number of contributors')]

    def extract_features(self) -> [Feature]:
        contributors = self.api_repo.get_contributors()
        num = len([c for c in contributors])
        self.features[0].value = num
        return self.features


class ForkExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Number of forks')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.api_repo.forks
        return self.features


class HasBuildFileExtractor(FeatureExtractor):
    # TODO: Add more build files
    build_files = ['build.gradle', 'composer.json', 'makefile' 'package.json', 'pom.xml']

    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Has build file')]

    def extract_features(self) -> [Feature]:
        try:
            files = self.api_repo.get_dir_contents('')
        except GithubException:
            files = []

        self.features[0].value = 0
        for file in files:
            if file.name and file.name.lower() in self.build_files:
                self.features[0].value = 1
        return self.features


class HasDownloadsExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Has downloads')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = 1 if self.api_repo.has_downloads else 0
        return self.features


class HasIssuesExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Has issues')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = 1 if self.api_repo.has_issues else 0
        return self.features


class HasWikiExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Has wiki')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = 1 if self.api_repo.has_wiki else 0
        return self.features


class IsForkExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Is a fork')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = 1 if self.api_repo.fork else 0
        return self.features


class DescriptionKeyWordExtractor(FeatureExtractor):
    # TODO: Add more keywords
    keywords = ['homework', 'lecture', 'course', 'framework', 'assignment', 'application', 'api', 'webapp']

    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature('Contains keyword "' + keyword + '"') for keyword in self.keywords]

    def extract_features(self):
        description = self.api_repo.description.lower() if self.api_repo.description else ''

        for keyword, feature in zip(self.keywords, self.features):
            if keyword in description:
                feature.value = 1
            else:
                feature.value = 0
        return self.features


class OpenIssueExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Number of open issues')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.api_repo.open_issues_count
        return self.features


class SizeExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Size of repo')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.api_repo.size
        return self.features


class StarExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Number of stars')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.api_repo.stargazers_count
        return self.features


class TotalFilesExtractor(FeatureExtractor):
    """
    Extractor for returning the total number of files for the default branch of the repository.
    """

    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Number of files')]

    def extract_features(self) -> [Feature]:
        # Boolean flag -> recursive call for contents
        total_num_files = self._get_num_files(self.api_repo.get_git_tree(self.repo.default_branch, True))
        self.features[0].value = total_num_files
        return self.features

    def _get_num_files(self, tree: GitTree) -> int:
        num_files = 0
        for item in tree.tree:
            if item.type == 'blob':
                num_files += 1
                # Because of recursive call ignore dirs seems to be working also with folders with 10000 files
        return num_files


class WatchersExtractor(FeatureExtractor):
    def __init__(self, repo: Repository):
        super().__init__(repo)
        self.features = [Feature(name='Number of watchers')]

    def extract_features(self) -> [Feature]:
        self.features[0].value = self.api_repo.watchers_count
        return self.features
