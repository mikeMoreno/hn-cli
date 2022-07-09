import requests
import click
import math
import webbrowser
from bs4 import BeautifulSoup


class SubmissionInfo:
    def __init__(self):
        self.id = None
        self.rank = None
        self.title = None

def get_title_text(title_info):
    title_text = title_info.text
    
    last_paren_index = title_text.rfind("(")
    
    if last_paren_index < 0:
        return title_text
    
    return title_text[:last_paren_index]

def get_title_info(submission):
    title_index = 0
    
    for child in submission.find_all(recursive=False):
         if "class" in child.attrs and child.attrs["class"][0] == "title":
            title_index+= 1
            
         if title_index == 2:
            return child
    return None
    
def parse_article_link(title_info):

    article_link = title_info.find_all("a")[0].attrs["href"]
    
    if not article_link.startswith("http"):
        article_link = f"https://news.ycombinator.com/{article_link}"
    
    return article_link
    
def get_rank(submission):
    title_index = 0
    
    for child in submission.find_all(recursive=False):
         if "class" in child.attrs and child.attrs["class"][0] == "title":
            title_index+= 1
            
         if title_index == 1:
            rank = child.text
            
            if rank is None:
                return None
            return int(rank.replace(".", "").strip())
            
    return None

def get_submission_info(submission):
    
    submission_info = SubmissionInfo()
    
    submission_info.id = submission.attrs["id"]
    
    submission_info.rank = get_rank(submission)
    
    title_info = get_title_info(submission)
    
    submission_info.title = get_title_text(title_info)
    submission_info.article_link = parse_article_link(title_info)
    
    return submission_info
    
def get_article_link(page, rank):

    doc = requests.get(f'https://news.ycombinator.com/news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")
    
    submissions = soup.select(".athing")

    for submission in submissions:
        submission_info = get_submission_info(submission)
        
        if submission_info.rank == rank:
            return submission_info.article_link
    return None
    
def get_submission_link(page, rank):

    doc = requests.get(f'https://news.ycombinator.com/news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")
    
    submissions = soup.select(".athing")

    for submission in submissions:
        submission_info = get_submission_info(submission)
        
        # TODO: move submission link to submission info object
        if submission_info.rank == rank:
            return f"https://news.ycombinator.com/item?id={submission_info.id}"
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
    doc = requests.get(f'https://news.ycombinator.com/news?p={page}', timeout=2)

    soup = BeautifulSoup(doc.text, "html.parser")
    
    submissions = soup.select(".athing")
    
    for submission in submissions:
        submission_info = get_submission_info(submission)
        
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
