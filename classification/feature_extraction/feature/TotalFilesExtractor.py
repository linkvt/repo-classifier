from github.GitTree import GitTree

from classification.Feature import Feature
from classification.feature_extraction.FeatureExtractor import FeatureExtractor


class TotalFilesExtractor(FeatureExtractor):
    """
    Extractor for returning the total number of files for the default branch of the repository.
    TODO needs testing with num files > 1000 in one folder because the API limits the recursive call to 1000.
    TODO testing file sizes > 1mb
    """
    def extract_features(self) -> [Feature]:
        # Not sure if master is always the best approach. Maybe it is better to request the latest commit and use the
        # SHA of it
        tree = self._repo.get_git_tree('master')
        assert isinstance(tree, GitTree), tree

        total_num_files = self._get_num_files(tree)
        return [Feature('Number of files: ', total_num_files)]

    def _get_num_files(self, tree: GitTree) -> int:
        num_files = 0
        for item in tree.tree:
            if item.type == 'blob':
                num_files += 1
            else:
                num_files += self._get_num_files(item)
        return num_files
