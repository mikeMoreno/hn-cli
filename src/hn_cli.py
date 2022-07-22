import os
import sys
import webbrowser
import click
import jsonpickle
from hn_client import HNClient
from submission_parser import SubmissionParser

class HNCli:

    def __init__(self, hn_client, **kwargs):
        self.hn_client = hn_client
        self.cache_file = HNCli._get_absolute_cache_file_path(kwargs["cache_file"])
        self.cache = kwargs["cache"]

        if not self.cache and os.path.isfile(self.cache_file):
            os.remove(self.cache_file)

    @staticmethod
    def _get_absolute_cache_file_path(cache_file):

        script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        absolute_cache_file_path = os.path.join(script_directory, cache_file)

        return absolute_cache_file_path

    @staticmethod
    def _format_rank(submission_rank):
        rank = f"[{submission_rank}]"

        if submission_rank < 10:
            rank = f" {rank}"

        return rank

    @staticmethod
    def _format_points(submission_points, highest_point_digits):
        points = f"{submission_points}|"

        while len(str(points)) <= highest_point_digits:
            points = " " + points
        points = "|" + points

        return points

    @classmethod
    def _format_submission(cls, submission_info, highest_point_digits):

        rank = HNCli._format_rank(submission_info.rank)
        points = HNCli._format_points(submission_info.points, highest_point_digits)

        return f"{rank} {points} {submission_info.title}"

    def _get_submission_info(self, rank):
        if os.path.isfile(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as submission_file:
                submissions = jsonpickle.decode(submission_file.read())
                submission_info = next(iter([s for s in submissions if s.rank == rank]), None)
        else:
            submission_info = self.hn_client.get_submission(rank)

        return submission_info

    def display_karma(self, profile):
        karma = self.hn_client.get_karma(profile)

        if karma is not None:
            print(karma)

    def display_articles(self, ranks):

        for rank in ranks:
            submission_info = self._get_submission_info(rank)

            webbrowser.open(submission_info.article_link)

    def display_submissions(self, ranks):

        for rank in ranks:
            submission_info = self._get_submission_info(rank)

            webbrowser.open(submission_info.submission_link)

    def display_all_submissions(self, page):

        submissions = self.hn_client.get_submissions(page)

        picked_submissions = jsonpickle.encode(submissions)

        if self.cache:
            with open(self.cache_file, "w", encoding="utf-8") as submission_file:
                submission_file.write(picked_submissions)

        highest_point_digits = len(str(max(s.points for s in submissions)))

        for submission in submissions:
            print(HNCli._format_submission(submission, highest_point_digits))

@click.command()
@click.option('--page', "-p", type=int, default=1, show_default=True, help="Display the specified page")
@click.option('--article', "-a", "articles", type=int, multiple=True, help="Open the specified article")
@click.option('--submission', "-s", "submissions", type=int, multiple=True, help="Open the specified submission")
@click.option('--karma', "-k", "profile", help="Display the karma of the specified profile")
@click.option('--cache/--no-cache', default=True, show_default=True, help="Cache the submission results")
def main(page, submissions, articles, profile, cache):

    HN_BASE_URL = "https://news.ycombinator.com/" # pylint: disable=invalid-name

    submission_parser = SubmissionParser(HN_BASE_URL)
    hn_client = HNClient(HN_BASE_URL, submission_parser)

    hn_cli = HNCli(hn_client, cache_file="submissions.json", cache=cache)

    if profile:
        hn_cli.display_karma(profile)

        return

    if articles:
        hn_cli.display_articles(articles)

    if submissions:
        hn_cli.display_submissions(submissions)

    if not articles and not submissions:
        hn_cli.display_all_submissions(page)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
