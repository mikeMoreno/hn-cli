from bs4 import BeautifulSoup
from submission_parser import SubmissionParser

HN_BASE_URL = "https://news.ycombinator.com/" # pylint: disable=invalid-name

def test_get_submission_info_properties_mapped():

    # Arrange
    submission_element = """
        <tr class="athing" id="32035875">
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
                <a class="titlelink" href="https://www.lg.com/us/monitors/lg-28mq780-b">LG 28-inch 16:18 DualUp Monitor</a>
                <span class="sitebit comhead"> (<a href="from?site=lg.com">
                        <span class="sitestr">lg.com</span>
                    </a>)</span>
            </td>
        </tr>
    """
    soup = BeautifulSoup(submission_element, 'html.parser')
    submission_element = soup.find_all()[0]
    
    score_element = '<span class="score" id="score_32045763">221 points</span>'
    soup = BeautifulSoup(score_element, 'html.parser')
    score_element = soup.find_all()[0]
    
    # Act
    submission_parser = SubmissionParser(HN_BASE_URL)

    submission_info = submission_parser.get_submission_info(submission_element, score_element)

    # Assert
    assert submission_info.id == "32035875"
    assert submission_info.rank == 1
    assert submission_info.points == 221
    assert submission_info.title == "LG 28-inch 16:18 DualUp Monitor"
    assert submission_info.article_link == "https://www.lg.com/us/monitors/lg-28mq780-b"
    assert submission_info.submission_link == f"{HN_BASE_URL}item?id=32035875"

def test_get_submission_info_submission_without_article_link():

    # Arrange
    submission_element = """
        <tr class="athing" id="32035875">
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
                <a class="titlelink" href="item?id=32030400">LG 28-inch 16:18 DualUp Monitor</a>
                <span class="sitebit comhead"> (<a href="from?site=lg.com">
                        <span class="sitestr">lg.com</span>
                    </a>)</span>
            </td>
        </tr>
    """
    soup = BeautifulSoup(submission_element, 'html.parser')
    submission_element = soup.find_all()[0]
    
    score_element = '<span class="score" id="score_32045763">221 points</span>'
    soup = BeautifulSoup(score_element, 'html.parser')
    score_element = soup.find_all()[0]

    # Act
    submission_parser = SubmissionParser(HN_BASE_URL)

    submission_info = submission_parser.get_submission_info(submission_element, score_element)

    # Assert
    assert submission_info.article_link == f"{HN_BASE_URL}item?id=32030400"
