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

def display_article(hn_client, article):
    submission_info = hn_client.get_submission(article)
    webbrowser.open(submission_info.article_link)

def display_submission(hn_client, submission):
    submission_info = hn_client.get_submission(submission)
    webbrowser.open(submission_info.submission_link)

def display_submissions(hn_client, page, hide_ranks):

    submissions = hn_client.get_submissions(page)

    for submission in submissions:
        print(format_submission(submission, hide_ranks))

@click.command()
@click.option('--page', "-p", type=int, default=1, show_default=True, help="Specify the page to display")
@click.option('--article', "-a", type=int, help="Specify the article to open")
@click.option('--submission', "-s", type=int, help="Specify the submission to open")
@click.option('--hide-ranks', is_flag=True, default=False, help="Hide ranks on output")
def main(page, submission, article, hide_ranks):

    HN_BASE_URL = "https://news.ycombinator.com/" # pylint: disable=invalid-name

    submission_parser = SubmissionParser(HN_BASE_URL)
    hn_client = HNClient(HN_BASE_URL, submission_parser)

    if article is not None:
        display_article(hn_client, article)

        return

    if submission is not None:
        display_submission(hn_client, submission)

        return

    display_submissions(hn_client, page, hide_ranks)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
