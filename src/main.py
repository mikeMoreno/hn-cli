import math
import webbrowser
import requests
import click
from bs4 import BeautifulSoup
from submission_parser import SubmissionParser

HN_BASE_URL = "https://news.ycombinator.com/"

def get_article_link(page, rank):

    doc = requests.get(f'{HN_BASE_URL}news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")

    submissions = soup.select(".athing")

    for submission in submissions:
        submission_info = SubmissionParser.get_submission_info(submission)

        if submission_info.rank == rank:
            return submission_info.article_link
    return None

def get_submission_link(page, rank):

    doc = requests.get(f'{HN_BASE_URL}news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")

    submissions = soup.select(".athing")

    for submission in submissions:
        submission_info = SubmissionParser.get_submission_info(submission)

        # TODO: move submission link to submission info object
        if submission_info.rank == rank:
            return f"{HN_BASE_URL}item?id={submission_info.id}"
    return None

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
        
def get_submission_info(page, rank):
    doc = requests.get(f'{HN_BASE_URL}news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")

    submissions = soup.select(".athing")

    for submission in submissions:
        submission_info = SubmissionParser.get_submission_info(submission)

        if submission_info.rank == rank:
            return submission_info
    return None

@click.command()
@click.option('--page', "-p", type=int, help="Specify the page to display")
@click.option('--article', "-a", type=int, help="Specify the article to open")
@click.option('--submission', "-s", type=int, help="Specify the submission to open")
@click.option('--hide-ranks', is_flag=True, default=False, help="Hide ranks on output")
def main(page, submission, article, hide_ranks):
    SUBMISSIONS_PER_PAGE = 30 # pylint: disable=invalid-name

    if page is not None:
        display_submissions(page, hide_ranks)

        return

    if article is not None:
        page = math.ceil(article / (SUBMISSIONS_PER_PAGE * 1.0))

        submission_info = get_submission_info(page, article)
        
        webbrowser.open(submission_info.article_link)
        return

    if submission is not None:
        page = math.ceil(submission / (SUBMISSIONS_PER_PAGE * 1.0))

        submission_info = get_submission_info(page, submission)
        
        webbrowser.open(submission_info.submission_link)

        return

    display_submissions(page, hide_ranks)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
