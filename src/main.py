import math
import webbrowser
import requests
import click
from bs4 import BeautifulSoup
from submission_parser import SubmissionParser

HN_BASE_URL = "https://news.ycombinator.com/"

def get_submissions(page):
    doc = requests.get(f'{HN_BASE_URL}news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")

    submission_elements = soup.select(".athing")

    submissions = []

    for submission_element in submission_elements:
        submission_info = SubmissionParser.get_submission_info(submission_element)
        submissions.append(submission_info)

    return submissions

def display_submission(submission_info, hide_ranks):

    if hide_ranks:
        return f"{submission_info.title}"

    rank = f"[{submission_info.rank}]"

    if submission_info.rank < 10:
        rank = f" {rank}"
    return f"{rank} {submission_info.title}"

def display_submissions(page, hide_ranks):

    submissions = get_submissions(page)

    for submission in submissions:
        print(display_submission(submission, hide_ranks))

def get_submission_info(rank):
    SUBMISSIONS_PER_PAGE = 30 # pylint: disable=invalid-name

    page = math.ceil(rank / (SUBMISSIONS_PER_PAGE * 1.0))

    doc = requests.get(f'{HN_BASE_URL}news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")

    submissions = soup.select(".athing")

    for submission in submissions:
        submission_info = SubmissionParser.get_submission_info(submission)

        if submission_info.rank == rank:
            return submission_info
    return None

@click.command()
@click.option('--page', "-p", type=int, default=1, show_default=True, help="Specify the page to display")
@click.option('--article', "-a", type=int, help="Specify the article to open")
@click.option('--submission', "-s", type=int, help="Specify the submission to open")
@click.option('--hide-ranks', is_flag=True, default=False, help="Hide ranks on output")
def main(page, submission, article, hide_ranks):

    if article is not None:
        submission_info = get_submission_info(article)

        webbrowser.open(submission_info.article_link)
        return

    if submission is not None:
        submission_info = get_submission_info(submission)

        webbrowser.open(submission_info.submission_link)

        return

    display_submissions(page, hide_ranks)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
