import requests
import click
import math
import webbrowser
from bs4 import BeautifulSoup
from SubmissionParser import *

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
    
def format(submission_info, hide_ranks):
        
    if hide_ranks:
        return f"{submission_info.title}"
    else:
        rank = f"[{submission_info.rank}]"
        
        if submission_info.rank < 10:
            rank = f" {rank}"
        return f"{rank} {submission_info.title}"

def display_submissions(page = 1, hide_ranks = False):
    doc = requests.get(f'{HN_BASE_URL}news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")
    
    submissions = soup.select(".athing")
    
    for submission in submissions:
        submission_info = SubmissionParser.get_submission_info(submission)
        
        print(format(submission_info, hide_ranks))
        
@click.command()
@click.option('--page', "-p", type=int, help="Specify the page to display")
@click.option('--article', "-a", type=int, help="Specify the article to open")
@click.option('--submission', "-s", type=int, help="Specify the submission to open")
@click.option('--hide-ranks', is_flag=True, default=False, help="Hide ranks on output")
def main(page, submission, article, hide_ranks):
    SUBMISSIONS_PER_PAGE = 30
    
    if page is not None:
        display_submissions(page, hide_ranks)
        
        return
        
    if article is not None:
        page = math.ceil(article / (SUBMISSIONS_PER_PAGE * 1.0))
        
        link = get_article_link(page, article)
        
        webbrowser.open(link)
        
        return
    
    if submission is not None:
        page = math.ceil(submission / (SUBMISSIONS_PER_PAGE * 1.0))
        
        link = get_submission_link(page, submission)

        webbrowser.open(link)

        return        

    display_submissions(hide_ranks = hide_ranks)
    
if __name__ == '__main__':
    main()
