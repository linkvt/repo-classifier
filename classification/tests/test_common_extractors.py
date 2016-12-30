from django.test import TestCase

from classification.feature_extraction.common import TotalFilesExtractor, CommitNumberExtractor
from classification.tests.GithubInitializerForTest import GithubInitializerForTest

# TODO probably create a own repository with individual content to test various setups
TEST_REPOSITORY = 'rmccue/test-repository'
OWN_REPO = 'BlackDark/InformatiCup2017TestRepo'


class TestTotalFilesExtractor(TestCase):
    def test_extract_features(self):
        repo = GithubInitializerForTest.get_connection().get_repo(OWN_REPO)
        extracted_features = TotalFilesExtractor(repo).extract_features()
        self.assertEqual(len(extracted_features), 1)
        self.assertEqual(extracted_features.pop().value, 11018, 'File num is incorrect')


class TestCommitNumberExtractor(TestCase):
    def test_extract_features(self):
        repo = GithubInitializerForTest.get_connection().get_repo(TEST_REPOSITORY)
        extracted_features = CommitNumberExtractor(repo).extract_features()
        self.assertEqual(len(extracted_features), 1)
        self.assertEqual(extracted_features.pop().value, 3, 'Commit number incorrect')
