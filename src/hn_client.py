import math
from bs4 import BeautifulSoup
import requests
from profile import Profile

class HNClient:

    def __init__(self, hn_base_url, submission_parser):
        self.hn_base_url = hn_base_url
        self.submission_parser = submission_parser

    def get_karma(self, id):
        doc = requests.get(f"{self.hn_base_url}user?id={id}", timeout=2)

        soup = BeautifulSoup(doc.text, "html.parser")

        profile_form = soup.find(id="hnmain")

        if profile_form is None:
            return None

        profile_text = profile_form.text.replace(" ", "")

        karma = None

        next = False

        for line in profile_text.split("\n"):
            if next:
                karma = line.strip()
                break
            if line.strip() == "karma:":
                next = True
        return int(karma)

    def get_submissions(self, page):
        doc = requests.get(f"{self.hn_base_url}news?p={page}", timeout=2)

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
