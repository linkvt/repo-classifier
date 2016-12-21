from unittest import TestCase

from classification.feature_extraction.common import TotalFilesExtractor, CommitNumberExtractor
from classification.tests.GithubInitializerForTest import GithubInitializerForTest

# TODO probably create a own repository with individual content to test various setups
TEST_REPOSITORY = 'rmccue/test-repository'


class TestTotalFilesExtractor(TestCase):
    def test_extract_features(self):
        repo = GithubInitializerForTest.get_connection().get_repo(TEST_REPOSITORY)
        extracted_features = TotalFilesExtractor(repo).extract_features()
        assert len(extracted_features) == 1
        assert extracted_features.pop().value == 2


class TestCommitNumberExtractor(TestCase):
    def test_extract_features(self):
        repo = GithubInitializerForTest.get_connection().get_repo(TEST_REPOSITORY)
        extracted_features = CommitNumberExtractor(repo).extract_features()
        assert len(extracted_features) == 1
        assert extracted_features.pop().value == 3
