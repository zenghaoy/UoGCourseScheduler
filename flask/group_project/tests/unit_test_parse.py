import unittest
import urllib.request
import re

from src.parse import buildTrdict

class parseJSONTest(unittest.TestCase):

    url = 'file:test.html'

    data = {
        "sections" : []
    }
    req = urllib.request.Request(url)      
    resp = urllib.request.urlopen(req)    
   
    respData = resp.read()
    tables = re.findall(r'<table summary="Sections">(.*?)</table>', str(respData))
  
    for tbody in tables:
        trs = re.findall(r'<tr ?.*?>(.*?)</tr>', str(tbody))
        for tr in trs:
            if '<td class=\"windowIdx\">' in tr:
                data["sections"].append(buildTrdict(tr))

    #close
    resp.close() 

    # check total amount of items
    def test_number_of_items(self):
        self.assertEqual(len(self.data['sections']),3036,"should be 3036")
    

    # check if each item matches
    def test_full_info(self):
        self.assertEqual(self.data['sections'][0]['course_code'],'ACCT*1220',"should be ACCT*1220")
        self.assertEqual(self.data['sections'][0]['course_name'],'Intro Financial Accounting',"should be Intro Financial Accounting")
        self.assertEqual(self.data['sections'][0]['section_code'],'0101',"should be 0101")
        self.assertEqual(self.data['sections'][0]['section_number'],'(6573)',"should be 6573")
        self.assertEqual(self.data['sections'][0]['term'],'Fall 2022',"should be Fall 2022")
        self.assertEqual(self.data['sections'][0]['status'],'Open',"should be Open")
        self.assertEqual(self.data['sections'][0]['location'],'Guelph',"should be Guelph")

        # total number of meeting_information
        self.assertEqual(len(self.data['sections'][0]['meeting_information']),3,"should be 3")

        # meeting_information without TBA value
        self.assertEqual(self.data['sections'][0]['meeting_information'][0]["dates"],'2022/09/08-2022/12/16',"should be 2022/09/08-2022/12/16")
        self.assertEqual(self.data['sections'][0]['meeting_information'][0]["type"],'LEC',"should be LEC")
        self.assertEqual(self.data['sections'][0]['meeting_information'][0]["days"][0],'Fri',"should be Fri")
        self.assertEqual(self.data['sections'][0]['meeting_information'][0]["time"],'08:30AM-10:20AM',"should be 08:30AM-10:20AM")
        self.assertEqual(self.data['sections'][0]['meeting_information'][0]["building"],'ROZH',"should be ROZH")
        self.assertEqual(self.data['sections'][0]['meeting_information'][0]["room"],'104',"should be 104")

        self.assertEqual(self.data['sections'][0]['faculty'],'P. Lassou',"should be P. Lassou")
        self.assertEqual(self.data['sections'][0]['available_capacity'],'3',"should be 3")
        self.assertEqual(self.data['sections'][0]['max_capacity'],'48',"should be 48")
        self.assertEqual(self.data['sections'][0]['credits'],'0.50',"should be 0.5")
        self.assertEqual(self.data['sections'][0]['academic_level'],'Undergraduate',"should be Undergraduate")


    # check meeting_information with TBA value
    def test_meeting_info_without_TBA(self):
        self.assertEqual(self.data['sections'][88]['meeting_information'][0]["dates"],'2022/09/08-2022/12/16',"should be 2022/09/08-2022/12/16")
        self.assertEqual(self.data['sections'][88]['meeting_information'][0]["type"],'TBA',"should be TBA")
        self.assertEqual(self.data['sections'][88]['meeting_information'][0]["days"],'TBA',"should be TBA")
        self.assertEqual(self.data['sections'][88]['meeting_information'][0]["time"],'TBA',"should be TBA")
        self.assertEqual(self.data['sections'][88]['meeting_information'][0]["building"],'TBA',"should be TBA")
        self.assertEqual(self.data['sections'][88]['meeting_information'][0]["room"],'TBA',"should be TBA")
    
    # check with max capacity and available capacity of 0
    def test_both_capactiy_of_zero(self):
        self.assertEqual(self.data['sections'][1368]['course_code'],'FOOD*3030',"should be FOOD*3030")
        self.assertEqual(self.data['sections'][1368]['available_capacity'],'0',"available capacity should be 0")
        self.assertEqual(self.data['sections'][1368]['max_capacity'],'0',"max capacity should be 0")
    
    # check with TBA faculty
    def test_TBA_faculty(self):
        self.assertEqual(self.data['sections'][88]['course_code'],'ANSC*6330',"should be ANSC*6330")
        self.assertEqual(self.data['sections'][88]['faculty'],'TBA  TBA',"should be TBA  TBA")

    def test_number_of_all_types(self):
        testSet = set()
        for item in self.data['sections']:
            testSet.add(item['meeting_information'][0]['type'])
        self.assertEqual(len(testSet),11,"should be 11")
        

if __name__ == "__main__":
    unittest.main()
