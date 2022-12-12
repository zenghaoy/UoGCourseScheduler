import json
import urllib.request

url = urllib.request.urlopen('https://cis3760team204.com/api/fall22')


def test_headerInfo():
    assert url.getcode() == 200


def test_bodyInfo():
    data = json.loads(url.read().decode())

    # total number of courses
    assert len(data['sections']) == 3036

    # first course info
    n = 0
    assert data['sections'][n]['course_code'] == "ACCT*1220"
    assert data['sections'][n]['course_name'] == "Intro Financial Accounting"
    assert data['sections'][n]['section_code'] == "0101"
    assert data['sections'][n]['section_number'] == "(6573)"
    assert data['sections'][n]['term'] == "Fall 2022"
    assert len(data['sections'][n]['meeting_information']) == 3
    assert data['sections'][n]['meeting_information'][0]['dates']\
        == "2022/09/08-2022/12/16"
    assert len(data['sections'][n]['meeting_information'][0]['days']) == 1
    assert data['sections'][n]['meeting_information'][0]['room'] == "104"
    assert data['sections'][n]['academic_level'] == "Undergraduate"

    # last course info
    n = 3035
    assert data['sections'][n]['course_code'] == "ZOO*4920"
    assert data['sections'][n]['course_name'] == "Lab Studies in Ornithology"
    assert data['sections'][n]['section_code'] == "01"
    assert data['sections'][n]['section_number'] == "(9393)"
    assert data['sections'][n]['term'] == "Fall 2022"
    assert len(data['sections'][n]['meeting_information']) == 1
    assert data['sections'][n]['meeting_information'][0]['dates']\
        == "2022/09/08-2022/12/16"
    assert len(data['sections'][n]['meeting_information'][0]['days']) == 1
    assert data['sections'][n]['meeting_information'][0]['room'] == "2304"
    assert data['sections'][n]['academic_level'] == "Undergraduate"
