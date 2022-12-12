import json
import urllib.request

url = urllib.request.urlopen('https://cis3760team204.com/api/winter23')


def test_headerInfo():
    assert url.getcode() == 200


def test_bodyInfo():
    data = json.loads(url.read().decode())

    # total number of courses
    assert len(data['sections']) == 2792

    # first course info
    n = 0
    assert data['sections'][n]['course_code'] == "ACCT*1220"
    assert data['sections'][n]['course_name'] == "Intro Financial Accounting"
    assert data['sections'][n]['section_code'] == "0101"
    assert data['sections'][n]['section_number'] == "(1065)"
    assert data['sections'][n]['term'] == "Winter 2023"
    assert len(data['sections'][n]['meeting_information']) == 2
    assert len(data['sections'][n]['meeting_information'][0]['days']) == 1
    assert data['sections'][n]['meeting_information'][0]['room'] == "104"
    assert data['sections'][n]['meeting_information'][1]['dates']\
        == "2023/01/09-2023/04/25"
    assert data['sections'][n]['academic_level'] == "Undergraduate"

    # last course info
    n = 2791
    assert data['sections'][n]['course_code'] == "ZOO*4950"
    assert data['sections'][n]['course_name'] == "Lab Studies in Mammalogy"
    assert data['sections'][n]['section_code'] == "0102"
    assert data['sections'][n]['section_number'] == "(3873)"
    assert data['sections'][n]['term'] == "Winter 2023"
    assert len(data['sections'][n]['meeting_information']) == 2
    assert data['sections'][n]['meeting_information'][0]['dates']\
        == "2023/01/09-2023/04/25"
    assert data['sections'][n]['meeting_information'][0]['days'] == "TBA"
    assert data['sections'][n]['meeting_information'][0]['room'] == "TBA"
    assert data['sections'][n]['academic_level'] == "Undergraduate"
