from bs4 import BeautifulSoup
import requests
import requests_mock
from src.hn_client import HNClient
from src.submission_parser import SubmissionParser

HN_BASE_URL = "https://news.ycombinator.com/" # pylint: disable=invalid-name

@requests_mock.Mocker(kw='mock')
def test_get_submissions_submissions_returned(**kwargs):

    # Arrange
    submission_elements = get_submission_data()
    kwargs['mock'].get(f'{HN_BASE_URL}news?p={1}', text=submission_elements)

    # Act
    submission_parser = SubmissionParser(HN_BASE_URL)
    hn_client = HNClient(HN_BASE_URL, submission_parser)
    
    submissions = hn_client.get_submissions(1)

    # Assert
    assert len(submissions) == 2
    assert submissions[0].title == "Submission Title 1"
    assert submissions[1].title == "Submission Title 2"
    
@requests_mock.Mocker(kw='mock')
def test_get_submission_submission_returned(**kwargs):

    # Arrange
    submission_elements = get_submission_data()
    kwargs['mock'].get(f'{HN_BASE_URL}news?p={1}', text=submission_elements)

    # Act
    submission_parser = SubmissionParser(HN_BASE_URL)
    hn_client = HNClient(HN_BASE_URL, submission_parser)
    
    submission = hn_client.get_submission(2)

    # Assert
    assert submission.title == "Submission Title 2"
    
@requests_mock.Mocker(kw='mock')
def test_get_submission_page_2_submission_returned(**kwargs):

    # Arrange
    submission_elements = """<tr class="athing" id="15">
            <td align="right" class="title" valign="top">
                <span class="rank">31.</span>
            </td>
            <td class="votelinks" valign="top">
                <center>
                    <a href="vote?id=32035875&amp;how=up&amp;goto=news%3Fp%3D1" id="up_32035875">
                        <div class="votearrow" title="upvote">
                </div>
                    </a>
                </center>
            </td>
            <td class="title">
                <a class="titlelink" href="https://www.lg.com/us/monitors/lg-28mq780-b">Submission Title 31</a>
                <span class="sitebit comhead"> (<a href="from?site=lg.com">
                        <span class="sitestr">lg.com</span>
                    </a>)</span>
            </td>
        </tr>
        <tr class="athing" id="16">
            <td align="right" class="title" valign="top">
                <span class="rank">32.</span>
            </td>
            <td class="votelinks" valign="top">
                <center>
                    <a href="vote?id=32035875&amp;how=up&amp;goto=news%3Fp%3D1" id="up_32035875">
                        <div class="votearrow" title="upvote">
                </div>
                    </a>
                </center>
            </td>
            <td class="title">
                <a class="titlelink" href="https://www.lg.com/us/monitors/lg-28mq780-b">Submission Title 32</a>
                <span class="sitebit comhead"> (<a href="from?site=lg.com">
                        <span class="sitestr">lg.com</span>
                    </a>)</span>
            </td>
        </tr>
    """
    
    kwargs['mock'].get(f'{HN_BASE_URL}news?p={2}', text=submission_elements)

    # Act
    submission_parser = SubmissionParser(HN_BASE_URL)
    hn_client = HNClient(HN_BASE_URL, submission_parser)
    
    submission = hn_client.get_submission(32)

    # Assert
    assert submission.title == "Submission Title 32"

def get_submission_data():
    return """<tr class="athing" id="15">
            <td align="right" class="title" valign="top">
                <span class="rank">1.</span>
            </td>
            <td class="votelinks" valign="top">
                <center>
                    <a href="vote?id=32035875&amp;how=up&amp;goto=news%3Fp%3D1" id="up_32035875">
                        <div class="votearrow" title="upvote">
                </div>
                    </a>
                </center>
            </td>
            <td class="title">
                <a class="titlelink" href="https://www.lg.com/us/monitors/lg-28mq780-b">Submission Title 1</a>
                <span class="sitebit comhead"> (<a href="from?site=lg.com">
                        <span class="sitestr">lg.com</span>
                    </a>)</span>
            </td>
        </tr>
        <tr class="athing" id="16">
            <td align="right" class="title" valign="top">
                <span class="rank">2.</span>
            </td>
            <td class="votelinks" valign="top">
                <center>
                    <a href="vote?id=32035875&amp;how=up&amp;goto=news%3Fp%3D1" id="up_32035875">
                        <div class="votearrow" title="upvote">
                </div>
                    </a>
                </center>
            </td>
            <td class="title">
                <a class="titlelink" href="https://www.lg.com/us/monitors/lg-28mq780-b">Submission Title 2</a>
                <span class="sitebit comhead"> (<a href="from?site=lg.com">
                        <span class="sitestr">lg.com</span>
                    </a>)</span>
            </td>
        </tr>
    """
