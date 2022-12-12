import sys
import unittest
from src.search import *


class testSearch(unittest.TestCase):
        

    # course code
    def test_validCourseCode(self):
        v_course_ret = searchByCourseCode('CIS*3760')
        self.assertEqual( len(v_course_ret["sections"]),3)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*3760")

    def test_validCourseCode2(self):
        v_course_ret = searchByCourseCode('CIS*6660')
        self.assertEqual(len(v_course_ret["sections"]),2)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*6660")
    
    def test_validCourseCode3(self):
        v_course_ret = searchByCourseCode('cis*6660')
        self.assertEqual(len(v_course_ret["sections"]),2)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*6660")


    def test_invalidCourseCode(self):
        v_course_ret = searchByCourseCode(' 1 ')
        self.assertEqual(len(v_course_ret["sections"]) ,0)

    def test_invalidCourseCode2(self):
        v_course_ret = searchByCourseCode('CIS3760')
        self.assertEqual( len(v_course_ret["sections"]),0)

    def test_invalidCourseCode3(self):
        v_course_ret = searchByCourseCode('#')
        self.assertEqual( len(v_course_ret["sections"]),0)

    # course name
    def test_validCourseName(self):
        v_course_ret = searchByCourseName('Software Engineering')
        self.assertEqual( len(v_course_ret["sections"]),3)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*3760")

    def test_validCourseName2(self):
        v_course_ret = searchByCourseName(r'Human Computer Interaction')
        self.assertEqual(len(v_course_ret["sections"]),1)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*4300")

    def test_validCourseName3(self):
        v_course_ret = searchByCourseName(r'Software Reliability & Testing')
        self.assertEqual(len(v_course_ret["sections"]),1)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*4150")
    
    def test_validCourseName4(self):
        v_course_ret = searchByCourseName(r'sofTware reliabiLity & tesTIng')
        self.assertEqual(len(v_course_ret["sections"]),1)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*4150")

    def test_invalidCourseName(self):
        v_course_ret = searchByCourseName('##')
        self.assertEqual(len(v_course_ret["sections"]) ,0)

    def test_invalidCourseName2(self):
        v_course_ret = searchByCourseName('Software Reliability & Testings')
        self.assertEqual(len(v_course_ret["sections"]) ,0)
    
    # course Department
    def test_validCourseDepartment(self):
        v_course_ret = searchByCourseDepartment('CIS')
        self.assertEqual(len(v_course_ret["sections"]) ,121)
        for i in v_course_ret["sections"]:
            self.assertEqual("CIS" in i["course_code"] ,True)
    
    def test_validCourseDepartment2(self):
        v_course_ret = searchByCourseDepartment('cis')
        self.assertEqual(len(v_course_ret["sections"]) ,121)
        for i in v_course_ret["sections"]:
            self.assertEqual("CIS" in i["course_code"] ,True)

    def test_invalidCourseDepartment(self):
        v_course_ret = searchByCourseDepartment('1')
        self.assertEqual(len(v_course_ret["sections"]) ,0)

    def test_invalidCourseDepartment2(self):
        v_course_ret = searchByCourseDepartment('$')
        self.assertEqual(len(v_course_ret["sections"]) ,0)

    # course section
    def test_validCourseCodeSection(self):
        v_course_ret = searchByCourseSection('CIS*3760 0101')
        self.assertEqual(len(v_course_ret["sections"]) ,1)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*3760")
            self.assertEqual(i["section_code"] ,"0101")

    def test_validCourseCodeSection2(self):
        v_course_ret = searchByCourseSection('cis*3760 0101')
        self.assertEqual(len(v_course_ret["sections"]) ,1)
        for i in v_course_ret["sections"]:
            self.assertEqual(i["course_code"] ,"CIS*3760")
            self.assertEqual(i["section_code"] ,"0101")
    
    def test_invalidCourseCodeSection(self):
        v_course_ret = searchByCourseSection('CIS*3760 0104')
        self.assertEqual(len(v_course_ret["sections"]) ,0)
    
    def test_invalidCourseCodeSection2(self):
        v_course_ret = searchByCourseSection('CIS*37600101')
        self.assertEqual(len(v_course_ret["sections"]) ,0)
    
    def test_invalidCourseCodeSection3(self):
        v_course_ret = searchByCourseSection('CIS*3760-0101')
        self.assertEqual(len(v_course_ret["sections"]) ,0)


if __name__=='__main__':
    unittest.main()
