from classifier.GithubAuthentification import GithubAuthentification


class GithubInitializerForTest:
    connection = None

    @staticmethod
    def get_connection() -> GithubAuthentification:
        if not GithubInitializerForTest.connection:
            GithubInitializerForTest.connection = GithubAuthentification()
        return GithubInitializerForTest.connection
