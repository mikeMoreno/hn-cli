import webbrowser
import click
from hn_client import HNClient
from submission_parser import SubmissionParser

def format_rank(submission_rank):
    rank = f"[{submission_rank}]"

    if submission_rank < 10:
        rank = f" {rank}"

    return rank

def format_points(submission_points, highest_point_digits):
    points = f"{submission_points}|"

    while len(str(points)) <= highest_point_digits:
        points = " " + points
    points = "|" + points

    return points

def format_submission(submission_info, highest_point_digits):

    rank = format_rank(submission_info.rank)
    points = format_points(submission_info.points, highest_point_digits)

    return f"{rank} {points} {submission_info.title}"

def display_karma(hn_client, profile):
    karma = hn_client.get_karma(profile)

    if karma is not None:
        print(karma)

def display_article(hn_client, rank):
    submission_info = hn_client.get_submission(rank)
    webbrowser.open(submission_info.article_link)

def display_submission(hn_client, rank):
    submission_info = hn_client.get_submission(rank)
    webbrowser.open(submission_info.submission_link)

def display_submissions(hn_client, page):

    submissions = hn_client.get_submissions(page)

    highest_point_digits = len(str(max([s.points for s in submissions])))

    for submission in submissions:
        print(format_submission(submission, highest_point_digits))

@click.command()
@click.option('--page', "-p", type=int, default=1, show_default=True, help="Display the specified page")
@click.option('--article', "-a", type=int, help="Open the specified article")
@click.option('--submission', "-s", type=int, help="Open the specified submission")
@click.option('--karma', "-k", "profile", help="Display the karma of the specified profile")
def main(page, submission, article, profile):

    HN_BASE_URL = "https://news.ycombinator.com/" # pylint: disable=invalid-name

    submission_parser = SubmissionParser(HN_BASE_URL)
    hn_client = HNClient(HN_BASE_URL, submission_parser)

    if profile:
        display_karma(hn_client, profile)
        return

    if article:
        display_article(hn_client, article)

        return

    if submission:
        display_submission(hn_client, submission)

        return

    display_submissions(hn_client, page)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
