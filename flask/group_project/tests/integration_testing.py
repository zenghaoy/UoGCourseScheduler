import unittest
from src.search import *
from src.main import load_html

class maintoParseTest(unittest.TestCase):

    # pass argv array
    def test_main_to_parse(self):
        argv = []
        argv.append("src")
        argv.append("file:test.html")
        json_string = load_html(argv)
        self.assertEqual(len(json_string['sections']),3036,"should be 3036")
    

    def test_main_to_search(self):
        argv = []
        argv.append("src")
        argv.append("file:test.html")
        json_string = load_html(argv)
        
        #course code
        num = 0
        for var in json_string["sections"]:
            if ( ((var["course_code"]).upper() == "CIS*3760".upper()) ):
               num+=1
        v_course_ret = searchByCourseCode('CIS*3760')
        self.assertEqual( len(v_course_ret["sections"]),num,"should be the same")

        #course name
        num = 0
        for var in json_string["sections"]:
            if ( ((var["course_name"]).upper() == "Software Engineering".upper()) ):
               num+=1
        v_course_ret = searchByCourseName('Software Engineering')
        self.assertEqual( len(v_course_ret["sections"]),num,"should be the same")

        #course section
        num = 0
        for var in json_string["sections"]:
           if(var["course_code"].upper()==("CIS*3760 0101".split(" ")[0]).upper() and var["section_code"].upper()== ("CIS*3760 0101".split(" ")[1]).upper()):
               num+=1
        v_course_ret = searchByCourseSection('CIS*3760 0101')
        self.assertEqual( len(v_course_ret["sections"]),num,"should be the same")

        #course department
        num = 0
        for var in json_string["sections"]:
            if((var["course_code"].split("*")[0]).upper()=="CIS".upper()):
               num+=1
        v_course_ret = searchByCourseDepartment('CIS')
        self.assertEqual( len(v_course_ret["sections"]),num,"should be the same")

       
        
if __name__ == "__main__":
    unittest.main()
