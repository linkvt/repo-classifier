from django.test import TestCase

from classification.feature_extraction.common import TotalFilesExtractor, CommitNumberExtractor
from classification.feature_extraction.web import DescriptionContainsURLExtractor
from classification.models import Repository

TEST_REPOSITORY = 'https://github.com/rmccue/test-repository'
OWN_REPO = 'https://github.com/BlackDark/InformatiCup2017TestRepo'


class TestTotalFilesExtractor(TestCase):
    def test_extract_features(self):
        extracted_features = TotalFilesExtractor(get_repo(OWN_REPO)).extract()
        self.assertEqual(len(extracted_features), 1)
        self.assertEqual(extracted_features.pop().value, 11018, 'File num is incorrect')


class TestCommitNumberExtractor(TestCase):
    def test_extract_features(self):
        extracted_features = CommitNumberExtractor(get_repo(TEST_REPOSITORY)).extract()
        self.assertEqual(len(extracted_features), 1)
        self.assertEqual(extracted_features.pop().value, 3, 'Commit number incorrect')


class TestDescriptionURLExtractor(TestCase):
    def test_repo_with_url(self):
        repo_with_url = 'https://github.com/rmccue/test-repository'
        extracted_features = DescriptionContainsURLExtractor(get_repo(repo_with_url)).extract()
        self.assertEqual(len(extracted_features), 1)
        self.assertEqual(extracted_features.pop().value, 1, 'Should contain URL')

    def test_repo_without_url(self):
        repo_without_url = 'https://github.com/BlackDark/InformatiCup2017TestRepo'
        extracted_features = DescriptionContainsURLExtractor(get_repo(repo_without_url)).extract()
        self.assertEqual(len(extracted_features), 1)
        self.assertEqual(extracted_features.pop().value, 0, 'Should contain URL')


def get_repo(url):
    return Repository(url=url)
