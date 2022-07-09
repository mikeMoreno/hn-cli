import math
import requests
from bs4 import BeautifulSoup
from submission_info import SubmissionInfo

class SubmissionParser:

    def __init__(self, hn_base_url):
        self.hn_base_url = hn_base_url

    def _get_title_text(self, title_info):
        title_text = title_info.text

        last_paren_index = title_text.rfind("(")

        if last_paren_index < 0:
            return title_text

        return title_text[:last_paren_index]

    def _get_title_info(self, submission):
        title_index = 0

        for child in submission.find_all(recursive=False):
            if "class" in child.attrs and child.attrs["class"][0] == "title":
                title_index+= 1

            if title_index == 2:
                return child
        return None

    def _get_article_link(self, title_info):

        article_link = title_info.find_all("a")[0].attrs["href"]

        if not article_link.startswith("http"):
            article_link = f"{self.hn_base_url}{article_link}"

        return article_link

    def _get_rank(self, submission):
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

    def _get_submission_info(self, submission):

        submission_info = SubmissionInfo()

        submission_info.id = submission.attrs["id"]

        submission_info.rank = self._get_rank(submission)

        title_info = self._get_title_info(submission)

        submission_info.title = self._get_title_text(title_info)
        submission_info.article_link = self._get_article_link(title_info)
        submission_info.submission_link = f"{self.hn_base_url}item?id={submission_info.id}"

        return submission_info

    def get_submissions(self, page):
        doc = requests.get(f'{self.hn_base_url}news?p={page}', timeout=2)

        soup = BeautifulSoup(doc.text, "html.parser")

        submission_elements = soup.select(".athing")

        submissions = []

        for submission_element in submission_elements:
            submission_info = self._get_submission_info(submission_element)
            submissions.append(submission_info)

        return submissions

    def get_submission(self, rank):
        SUBMISSIONS_PER_PAGE = 30 # pylint: disable=invalid-name

        page = math.ceil(rank / (SUBMISSIONS_PER_PAGE * 1.0))

        submissions = self.get_submissions(page)

        return next(filter(lambda s: s.rank == rank, submissions), None)
