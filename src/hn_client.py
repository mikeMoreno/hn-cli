import math
import requests
from bs4 import BeautifulSoup

class HNClient:

    def __init__(self, hn_base_url, submission_parser):
        self.hn_base_url = hn_base_url
        self.submission_parser = submission_parser

    def get_submissions(self, page):
        doc = requests.get(f'{self.hn_base_url}news?p={page}', timeout=2)

        soup = BeautifulSoup(doc.text, "html.parser")

        submission_elements = soup.select(".athing")

        submissions = []

        for submission_element in submission_elements:
            submission_info = self.submission_parser.get_submission_info(submission_element)
            submissions.append(submission_info)

        return submissions

    def get_submission(self, rank):
        SUBMISSIONS_PER_PAGE = 30 # pylint: disable=invalid-name

        page = math.ceil(rank / (SUBMISSIONS_PER_PAGE * 1.0))

        submissions = self.get_submissions(page)

        return next(filter(lambda s: s.rank == rank, submissions), None)
