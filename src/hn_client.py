import math
from bs4 import BeautifulSoup
import requests

class HNClient:

    def __init__(self, hn_base_url, submission_parser):
        self.hn_base_url = hn_base_url
        self.submission_parser = submission_parser

    def get_karma(self, user_id):
        doc = requests.get(f"{self.hn_base_url}user?id={user_id}", timeout=2)

        soup = BeautifulSoup(doc.text, "html.parser")

        profile_form = soup.find(id="hnmain")

        if profile_form is None:
            return None

        profile_text = profile_form.text.replace(" ", "")

        karma = None

        next_line = False

        for line in profile_text.split("\n"):
            if next_line:
                karma = line.strip()
                break
            if line.strip() == "karma:":
                next_line = True
        return int(karma)

    def get_submissions(self, page):
        doc = requests.get(f"{self.hn_base_url}news?p={page}", timeout=2)

        soup = BeautifulSoup(doc.text, "html.parser")

        submission_tags = soup.select(".athing")
        score_tags = soup.select(".score")

        submissions = []

        for submissions_and_scores in zip(submission_tags, score_tags):
            submission_info = self.submission_parser.get_submission_info(submissions_and_scores[0], submissions_and_scores[1])
            submissions.append(submission_info)

        return submissions

    def get_submission(self, rank):
        SUBMISSIONS_PER_PAGE = 30 # pylint: disable=invalid-name

        page = math.ceil(rank / (SUBMISSIONS_PER_PAGE * 1.0))

        submissions = self.get_submissions(page)

        return next(filter(lambda s: s.rank == rank, submissions), None)
