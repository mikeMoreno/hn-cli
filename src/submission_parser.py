from src.submission_info import SubmissionInfo

class SubmissionParser:

    def __init__(self, hn_base_url):
        self.hn_base_url = hn_base_url

    def _get_title_text(self, title_info):
        title_text = title_info.text

        last_paren_index = title_text.rfind("(")

        if last_paren_index < 0:
            return title_text

        return title_text[:last_paren_index].strip()

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
    
        for child in submission.find_all(recursive=False):
            if "class" in child.attrs and child.attrs["class"][0] == "title":
                rank = child.text
                
                return int(rank.replace(".", "").strip())

        return None

    def get_submission_info(self, submission):

        submission_info = SubmissionInfo()

        submission_info.id = submission.attrs["id"]
        submission_info.rank = self._get_rank(submission)

        title_info = self._get_title_info(submission)

        submission_info.title = self._get_title_text(title_info)
        submission_info.article_link = self._get_article_link(title_info)
        submission_info.submission_link = f"{self.hn_base_url}item?id={submission_info.id}"

        return submission_info
