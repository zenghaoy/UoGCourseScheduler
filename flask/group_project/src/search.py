import json
from pickle import TRUE

def searchByCourseCode(course):
    return_data = {"sections" : []}

    with open('json_data.json', 'r') as infile:
        jsondata = json.load(infile)
    courses = jsondata["sections"]
    # convert 
    for var in courses:
        # search for name match in course code or in course name
        if ( ((var["course_code"]).upper() == course.upper()) ):
            return_data["sections"].append(var)

    return return_data
def searchByCourseName(course):
    return_data = {"sections" : []}

    with open('json_data.json', 'r') as infile:
        jsondata = json.load(infile)
    courses = jsondata["sections"]
    # convert 
    for var in courses:
        # search for name match in course code or in course name
        if ( ((var["course_name"]).upper() == course.upper()) ):
            return_data["sections"].append(var)

    return return_data

def searchByCourseDepartment(courseType):
    return_data = {"sections" : []}

    with open('json_data.json', 'r') as infile:
        jsondata = json.load(infile)
    courses = jsondata["sections"]
    for var in courses:
        if((var["course_code"].split("*")[0]).upper()==courseType.upper()):
            return_data["sections"].append(var)
    return return_data
    
def searchByCourseSection(courseCodeSection):
    return_data = {"sections" : []}

    with open('json_data.json', 'r') as infile:
        jsondata = json.load(infile)
    courses = jsondata["sections"]
    for var in courses:
        if(var["course_code"].upper()==(courseCodeSection.split(" ")[0]).upper() and var["section_code"].upper()== (courseCodeSection.split(" ")[1]).upper()):
            return_data["sections"].append(var)
    return return_data

def printCourse(courseData):
    
    print("-----------------------------------------------------------------------------------------------------------")
    print("Course:       "+courseData["academic_level"]+" "+courseData["course_code"]+" "+courseData["section_code"]+" "+courseData["course_name"] )
    print("Location:     "+courseData["location"])
    
    for var in courseData["meeting_information"]:
        
        # only display lab information if course has a lab
        days = ""

        if(var['days']!="TBA"):
            for day in var['days']:
                days += day +" "
        else:
            days="TBA "

        if(var['type']=='LEC'):
            print("Lectures:     "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='LAB'):
            print("Lab:          "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='EXAM'):
            print("Exam:         "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='SEM'):
            print("Seminar:      "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='Tutorial'):
            print("Tutorial:     "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='Reading'):
            print("Reading:      "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='Independent'):
            print("Independent:      "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='None'):
            print("No Data")
        if(var['type']=='Electronic'):
            print("Electronic:   "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='TBA'):
            print("TBA")
        if(var['type']=='Practicum'):
            print("Practicum:    "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])
        if(var['type']=='Distance'):
            print("DE:            "+"Building: "+var["building"]+" "+var["room"]+" Time: "+var["time"]+" Days: "+days+"Dates: "+var["dates"])

    print("Semester:     "+courseData["term"])
    print("Capacity:     "+courseData["available_capacity"]+"/"+courseData["max_capacity"])
    print("Prof:         "+courseData["faculty"])
    print("Credits:      "+courseData["credits"])
    print("Status:       "+courseData["status"])
    print("-----------------------------------------------------------------------------------------------------------")
    return 0
