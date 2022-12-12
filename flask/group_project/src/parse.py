import re
import json
import urllib.request

def html_replace(char_in):

    return char_in.replace("\\r","").replace("&amp;","&")

def load_html(argv):
    url = argv[1]               
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
    json_string = data
    with open('winter22_courses.json', 'w') as outfile:
        json.dump(json_string, outfile)
    outfile.close()
    return json_string

def buildTrdict(tr):
    single_tr = {}
    shortTitles = re.findall(r'<td class=" SEC_SHORT_TITLE .*?">(.*?)</td>', str(tr))
    for shortTitle in shortTitles:
        sectionNamesTitles = re.findall(r'<div>(.*?)</div>', str(shortTitle))
        for sectionNamesTitle in sectionNamesTitles:
            courseNameTitles = re.findall(r'<a .*?>(.*?)</a>', str(sectionNamesTitle))
            for courseNameTitle in courseNameTitles:
                single_tr["course_code"] = html_replace(courseNameTitle.split('*')[0] + "*" + courseNameTitle.split('*')[1])
                single_tr["course_name"] = html_replace(courseNameTitle.split(')')[1].strip())
                single_tr["section_code"] = html_replace(courseNameTitle.split('*')[2].split(' ')[0])
                single_tr["section_number"] = html_replace(courseNameTitle.split(' ')[1])
    
    windowIdxes = re.findall(r'<td class="windowIdx">(.*?)</td>', str(tr))
    courseSections = re.findall(r'<td class=" WSS_COURSE_SECTIONS .*?">(.*?)</td>', str(tr))
    meetings = re.findall(r'<td class=" SEC_MEETING_INFO .*?">(.*?)</td>', str(tr))
    faculties = re.findall(r'<td class=" SEC_FACULTY_INFO .*?">(.*?)</td>', str(tr))
    capacities = re.findall(r'<td class=" LIST_VAR5 .*?">(.*?)</td>', str(tr))
    credits = re.findall(r'<td class=" SEC_MIN_CRED .*?">(.*?)</td>', str(tr))
    academicLevels = re.findall(r'<td class=" SEC_ACAD_LEVEL .*?">(.*?)</td>', str(tr))    

    term = re.findall(r'<p id="WSS_COURSE_SECTIONS_[0-9]+">(.*?)</p>',str(tr))
    status = re.findall(r'<p id="LIST_VAR1_[0-9]+">(.*?)</p>',str(tr))
    faculty = re.findall(r'<p id="SEC_FACULTY_INFO_\d+">(.*?)</p>', str(tr))
    section_name_and_title = re.findall(r'<a class="left" id="SEC_SHORT_TITLE_[0-9]+".*?>(.*?)</a>',str(tr))
    location= re.findall(r'<p id="SEC_LOCATION_[0-9]+">(.*?)</p>',str(tr))
    meeting_information = re.findall(r'value="(.*?)"', str(meetings[0]))
    av_cap = re.findall(r'value=\"(.*?)\">',str(capacities[0]))
    cred = re.findall(r'value=\"(.*?)\">',str(credits[0]))
    academic = re.findall(r'value=\"(.*?)\">',str(academicLevels[0]))

    days_of_week = ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"]
    meeting_list = []
    for meeting_str in meeting_information[0].split('\\n'):
        dates = "TBA"
        meet_type = "TBA"
        days = []
        time = "TBA"
        building = "TBA"
        room = "TBA"
        dates = meeting_str.split(' ')[0]
        if(len(meeting_str.split(' ')) > 1):
            meet_type = meeting_str.split(' ')[1]
        count = 0
        if(len(meeting_str.split(' ')) > 2):
            for day in meeting_str.split(meet_type)[1].split(','):
                
                if day.strip().split(' ')[0].strip(',') in days_of_week:
                    days.append(day.strip().split(' ')[0].strip(','))
                    count += 1

                if (len(day.strip().split(' ')) == 2):
                    if day.strip().split(' ')[0] == 'Room':
                        room = day.strip().split(' ')[1]
                
                if (len(day.strip().split(' ')) < 2):
                    if (day.strip().split(' ')[0]) not in days_of_week:
                        building = day.strip().split(' ')[0]    

            if(meeting_str.split(meet_type)[1].split(',')[count-1].strip().split(' ')[0] in days_of_week):
                time = meeting_str.split(meet_type)[1].split(',')[count-1].strip().split(' ')[1] + \
                meeting_str.split(meet_type)[1].split(',')[count-1].strip().split(' ')[2] + \
                meeting_str.split(meet_type)[1].split(',')[count-1].strip().split(' ')[3]
        
        meeting_list.append({
                "dates" : html_replace(dates),
                "type" : html_replace(meet_type),
                "days" : days if len(days) != 0 else 'TBA',
                "time" : html_replace(time),
                "building" : html_replace(building),
                "room" : html_replace(room)
                })


    single_tr['term'] = html_replace(term[0])
    single_tr['status'] = html_replace(status[0])
    single_tr['location'] = html_replace(location[0])
    single_tr['meeting_information'] = (meeting_list)
    single_tr['faculty'] = html_replace(faculty[0])
    single_tr['available_capacity'] = av_cap[0].split(' ')[0] if len(av_cap[0]) != 0 else '0'
    single_tr['max_capacity'] = av_cap[0].split(' ')[2] if len(av_cap[0]) != 0 else '0'
    single_tr['credits'] = cred[0]
    single_tr['academic_level'] = html_replace(academic[0])
    return single_tr
