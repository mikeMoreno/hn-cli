from submission_info import SubmissionInfo

class SubmissionParser:

    @classmethod
    def _get_title_text(cls, title_info):
        title_text = title_info.text

        last_paren_index = title_text.rfind("(")

        if last_paren_index < 0:
            return title_text

        return title_text[:last_paren_index]

    @classmethod
    def _get_title_info(cls, submission):
        title_index = 0

        for child in submission.find_all(recursive=False):
            if "class" in child.attrs and child.attrs["class"][0] == "title":
                title_index+= 1

            if title_index == 2:
                return child
        return None

    @classmethod
    def _parse_article_link(cls, title_info):

        article_link = title_info.find_all("a")[0].attrs["href"]

        if not article_link.startswith("http"):
            article_link = f"https://news.ycombinator.com/{article_link}"

        return article_link

    @classmethod
    def _get_rank(cls, submission):
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

    @classmethod
    def get_submission_info(cls, submission):

        submission_info = SubmissionInfo()

        submission_info.id = submission.attrs["id"]

        submission_info.rank = cls._get_rank(submission)

        title_info = cls._get_title_info(submission)

        submission_info.title = cls._get_title_text(title_info)
        submission_info.article_link = cls._parse_article_link(title_info)

        return submission_info
