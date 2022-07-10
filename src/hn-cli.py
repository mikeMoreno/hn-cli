import webbrowser
import click
from hn_client import HNClient
from submission_parser import SubmissionParser

def format_submission(submission_info, hide_ranks):

    if hide_ranks:
        return f"{submission_info.title}"

    rank = f"[{submission_info.rank}]"

    if submission_info.rank < 10:
        rank = f" {rank}"
    return f"{rank} {submission_info.title}"

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

def display_submissions(hn_client, page, hide_ranks):

    submissions = hn_client.get_submissions(page)

    for submission in submissions:
        print(format_submission(submission, hide_ranks))

@click.command()
@click.option('--page', "-p", type=int, default=1, show_default=True, help="Display the specified page")
@click.option('--article', "-a", type=int, help="Open the specified article")
@click.option('--submission', "-s", type=int, help="Open the specified submission")
@click.option('--hide-ranks', is_flag=True, default=False, help="Hide ranks on output")
@click.option('--karma', "-k", "profile", help="Display the karma of the specified profile")
def main(page, submission, article, hide_ranks, profile):

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

    display_submissions(hn_client, page, hide_ranks)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
