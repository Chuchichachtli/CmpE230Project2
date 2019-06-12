#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
import csv
import time
starting = sys.argv[1]
ending = sys.argv[2]

codes = ["AD", "ASIA", "ASIA", "ATA", "AUTO", "BIO", "BIS", "BM", "CCS", "CE", "CEM", "CET", "CET", "CHE", "CHEM", "CMPE", "COGS", "CSE", "EC", "ED", "EE", "EF", "ENV", "ENVT", "EQE", "ETM", "FE", "FLED", "GED", "GPH", "GUID", "HIST", "HUM", "IE", "INCT", "INT", "INTT", "INTT", "LING", "LL", "LS", "MATH", "ME", "MECA", "MIR", "MIR", "MIS", "PA", "PE",  "PHIL", "PHYS", "POLS", "PRED", "PSY", "SCED", "SCED", "SCO", "SOC", "SPL", "SWE", "SWE", "TK", "TKL", "TR", "TRM", "TRM", "WTR", "XMBA", "YADYOK"]
codecnt=69
Names = ["MANAGEMENT","ASIAN+STUDIES","ASIAN+STUDIES+WITH+THESIS",
"ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY","AUTOMOTIVE+ENGINEERING",
"MOLECULAR+BIOLOGY+%26+GENETICS","BUSINESS+INFORMATION+SYSTEMS",
"BIOMEDICAL+ENGINEERING","CRITICAL+AND+CULTURAL+STUDIES",
"CIVIL+ENGINEERING","CONSTRUCTION+ENGINEERING+AND+MANAGEMENT",
"COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY","EDUCATIONAL+TECHNOLOGY",
"CHEMICAL+ENGINEERING","CHEMISTRY","COMPUTER+ENGINEERING","COGNITIVE+SCIENCE",
"COMPUTATIONAL+SCIENCE+%26+ENGINEERING","ECONOMICS","EDUCATIONAL+SCIENCES",
"ELECTRICAL+%26+ELECTRONICS+ENGINEERING","ECONOMICS+AND+FINANCE",
"ENVIRONMENTAL+SCIENCES","ENVIRONMENTAL+TECHNOLOGY",
"EARTHQUAKE+ENGINEERING","ENGINEERING+AND+TECHNOLOGY+MANAGEMENT",
"FINANCIAL+ENGINEERING","FOREIGN+LANGUAGE+EDUCATION","GEODESY","GEOPHYSICS","GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING",
"HISTORY","HUMANITIES+COURSES+COORDINATOR","INDUSTRIAL+ENGINEERING","INTERNATIONAL+COMPETITION+AND+TRADE",
"CONFERENCE+INTERPRETING","INTERNATIONAL+TRADE","INTERNATIONAL+TRADE+MANAGEMENT","LINGUISTICS","WESTERN+LANGUAGES+%26+LITERATURES",
"LEARNING+SCIENCES","MATHEMATICS","MECHANICAL+ENGINEERING","MECHATRONICS+ENGINEERING",
"INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST",
"INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS",
"MANAGEMENT+INFORMATION+SYSTEMS","FINE+ARTS","PHYSICAL+EDUCATION",
"PHILOSOPHY","PHYSICS","POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS","PRIMARY+EDUCATION",
"PSYCHOLOGY","MATHEMATICS+AND+SCIENCE+EDUCATION","SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION",
"SYSTEMS+%26+CONTROL+ENGINEERING","SOCIOLOGY","SOCIAL+POLICY+WITH+THESIS","SOFTWARE+ENGINEERING","SOFTWARE+ENGINEERING+WITH+THESIS",
"TURKISH+COURSES+COORDINATOR","TURKISH+LANGUAGE+%26+LITERATURE","TRANSLATION+AND+INTERPRETING+STUDIES",
"SUSTAINABLE+TOURISM+MANAGEMENT","TOURISM+ADMINISTRATION","TRANSLATION","EXECUTIVE+MBA","SCHOOL+OF+FOREIGN+LANGUAGES"]

namesToPrint = ["MANAGEMENT","ASIAN STUDIES","ASIAN STUDIES WITH THESIS","ATATURK INSTITUTE FOR MODERN TURKISH HISTORY","AUTOMOTIVE ENGINEERING",
"MOLECULAR BIOLOGY & GENETICS","BUSINESS INFORMATION SYSTEMS","BIOMEDICAL ENGINEERING","CRITICAL AND CULTURAL STUDIES","CIVIL ENGINEERING","CONSTRUCTION ENGINEERING AND MANAGEMENT","COMPUTER EDUCATION & EDUCATIONAL TECHNOLOGY","EDUCATIONAL TECHNOLOGY",
"CHEMICAL ENGINEERING","CHEMISTRY","COMPUTER ENGINEERING","COGNITIVE SCIENCE","COMPUTATIONAL SCIENCE & ENGINEERING","ECONOMICS",
"EDUCATIONAL SCIENCES","ELECTRICAL & ELECTRONICS ENGINEERING","ECONOMICS AND FINANCE","ENVIRONMENTAL SCIENCES","ENVIRONMENTAL TECHNOLOGY","EARTHQUAKE ENGINEERING",
"ENGINEERING AND TECHNOLOGY MANAGEMENT","FINANCIAL ENGINEERING","FOREIGN LANGUAGE EDUCATION","GEODESY","GEOPHYSICS","GUIDANCE & PSYCHOLOGICAL COUNSELING","HISTORY","HUMANITIES COURSES COORDINATOR","INDUSTRIAL ENGINEERING",
"INTERNATIONAL COMPETITION AND TRADE","CONFERENCE INTERPRETING","INTERNATIONAL TRADE","INTERNATIONAL TRADE MANAGEMENT","LINGUISTICS","WESTERN LANGUAGES & LITERATURES","LEARNING SCIENCES",
"MATHEMATICS","MECHANICAL ENGINEERING","MECHATRONICS ENGINEERING","INTERNATIONAL RELATIONS:TURKEY,EUROPE AND THE MIDDLE EAST","INTERNATIONAL RELATIONS:TURKEY,EUROPE AND THE MIDDLE EAST WITH THESIS","MANAGEMENT INFORMATION SYSTEMS",
"FINE ARTS","PHYSICAL EDUCATION","PHILOSOPHY","PHYSICS","POLITICAL SCIENCE&INTERNATIONAL RELATIONS","PRIMARY EDUCATION",
"PSYCHOLOGY","MATHEMATICS AND SCIENCE EDUCATION","SECONDARY SCHOOL SCIENCE AND MATHEMATICS EDUCATION","SYSTEMS & CONTROL ENGINEERING","SOCIOLOGY","SOCIAL POLICY WITH THESIS","SOFTWARE ENGINEERING","SOFTWARE ENGINEERING WITH THESIS",
"TURKISH COURSES COORDINATOR","TURKISH LANGUAGE & LITERATURE","TRANSLATION AND INTERPRETING STUDIES","SUSTAINABLE TOURISM MANAGEMENT","TOURISM ADMINISTRATION","TRANSLATION","EXECUTIVE MBA","SCHOOL OF FOREIGN LANGUAGES"]

#Tokenizes the arguments for the URL links
def getTime(time):
    year = ""
    donem = ""
    for letter in time:
        if letter == '-':
            break
        year += letter
    if "Fall" in time:
        donem = 1
    elif "Spring" in time:
        donem = 2 
    elif "Summer" in time:
        donem = 3
    int_year = int(year)
    return int_year, donem

#Removes the section code from the lesson code and returns the sectionless code and 
#if it's an undergrad or a grad lesson 0 if grad 1 if undergrad
def getLessonCode(STR): 
    a = ""
    flag = 0
    under = 1
    for letter in STR:
        if letter == '.':
            break
        if letter >= '0' and letter <= '9' and flag == 0:
            flag = 1

        if (letter >= '5' and letter <= '9') and flag == 1:
            flag = 1230
            under = 0
        elif letter <= '4':
            flag = 9
        a+=letter
    return a , under

# puts the code and the respective course
def linkertuple(codelist, courselist): 
    tuplelist = []
    i = 0
    for course in courselist:
        tuplelist.append([codelist[i], courselist[i]])
        i+=1
    return tuplelist


#Gets the page for the specified year, semester, department code and department name ( mp is for instructors -> dictionary of sets, keeps the instructors for distinc coursees )
def getPage(yil,donem,kisaad,bolum,mp):
    quote_page = "https://registration.boun.edu.tr/scripts/sch.asp?donem="+str(yil)+'/'+str(yil+1)+'-'+str(donem)+"&kisaadi="+kisaad+"&bolum="+bolum    


    while True: # try to request untill success
        try:
            page = requests.get(quote_page) #get page
            break
        except:
            time.sleep(1)

    soup = BeautifulSoup(page.text,"lxml") # Render with BeatifulSoup
#    print(quote_page)
    solmenu = soup.find_all("td") # just get <td> tags
    flag=0
    lesson_flag=0
    course_list = [] # course list with code names
    lesson_list = [] # course list with long names
    instructor_set = set() # instructor set
    instructor_count=0
    under_count=0
    graduate_count=0 

    firstcourse=1
    for link in solmenu:
        if flag==1:
#            print(link.text) # Lesson Name
            flag+=1
            if lesson_flag is 1:
                lesson_list.append(link.text.replace(u'\xa0','')) ## crop the end line char
            lesson_flag=0 
            continue
        if flag==4:
#            print(link.text) #instructor
            if link.text not in "STAFF" and link.text not in instructor_set:
                instructor_set.add(link.text)
                instructor_count+=1
            if link.text not in "STAFF":
                try:
                    mp[course_list[-1]].add(link.text)
                except KeyError:
                    mp[course_list[-1]] = set()
                    mp[course_list[-1]].add(link.text)

            flag=0
            continue
        if flag > 0:
            flag+=1
            continue
        if link.text in "Desc."  and  last not in "Code.Sec": # finds the Desc.  so the last is cource code
            last , UL =getLessonCode(last) # Gets without section , returns1 if under
            flag=1 # keep flag to find instructors of that course
            if last not in course_list: 
                course_list.append(last) # add to course
                lesson_flag=1
                if UL == 1:
                    under_count+=1
                else:
                    graduate_count+=1
            continue
        last = link.text
    return linkertuple(course_list,lesson_list),instructor_set , mp


# Returns the union of two lists. Without coppies
def Union(a, b):  
    newlist=[]
    for i in a:
        newlist.append(i)
    for z in b:
        if z not in newlist:
            newlist.append(z)
    newlist.sort()
    return newlist
#Under or Grad 
def UorL(STR): 
    flag = 0
    under = 1
    for letter in STR:
        if (letter >= '5' and letter <= '9') and flag == 0:
            under = 0
        if letter >= '0' and letter <= '9':
            flag = 1
        
    return under

def solveDep(kisaad,bolum,sy,sd,ey,ed):  #startyear, startdonem, endyear, enddonem
    total_courses=[]
    course_sets =[]
    total_instructor_set = set()
    instructor_sets = []
    mp = {}
#    print(kisaad,bolum,sy,sd,ey,ed)
    while 1: # gets , and calculates all the data
        courses,instructor_set ,mp=getPage(sy,sd,kisaad,bolum,mp)
        total_instructor_set.update(instructor_set)
        total_courses = Union ( total_courses , courses )
        course_sets.append(courses)
        instructor_sets.append(instructor_set)
        sd+=1
        if(sy==ey and sd==ed+1):
            break
        if(sd==4):
            sd=1
            sy+=1
    total_under_count=0
    total_graduate_count=0 
    for i in total_courses: # finds total undergraduate - graduate lesons count 
        if UorL(i[0]) == 1:
            total_under_count+=1
        else:
            total_graduate_count+=1

    total_offerings_under=0
    total_offerings_graduate=0
    total_offerings_instructor=0
    
    firstline = []
    indexOf = Names.index(bolum)
    realBolum = namesToPrint[indexOf]
    firstline.append(kisaad + " (" + realBolum + ")" ) 
    firstline.append("U"+str(total_under_count)+" G"+str(total_graduate_count))
    firstline.append("")
    for i in range(len(instructor_sets)): # finds the first line of every course , Total under-grad course etc.
        under_count=0
        graduate_count=0
        for j in course_sets[i]:
            if UorL(j[0]) == 1:
                under_count+=1
            else:
                graduate_count+=1
        firstline.append("U"+str(under_count)+" G"+str(graduate_count)+" I"+str(len(instructor_sets[i])))
        total_offerings_under+=under_count
        total_offerings_graduate+=graduate_count
        total_offerings_instructor+=len(instructor_sets[i])
    firstline.append("U"+str(total_offerings_under)+" G"+str(total_offerings_graduate)+" I"+str(len(total_instructor_set)))
    print(*firstline, sep = ", ")  

    for i in range(len(total_courses)): # fills other lines for the course
        line=[]
        line.append("")
        line.append(total_courses[i][0])
        line.append("\""+total_courses[i][1]+"\"")
        given = 0
        for j in course_sets:
            if total_courses[i] in j:
                line.append("x")
                given += 1
            else:
                line.append(" ")
        try:
            line.append(str(given)+"/"+str(len(mp[total_courses[i][0]])))
        except KeyError:
            mp[total_courses[i][0]]=set()
            line.append(str(given)+"/"+str(len(mp[total_courses[i][0]])))
        print(*line, sep = ", ")  

sy,sd = getTime(starting)  #start year, start semester
ey,ed = getTime(ending)    #end year , end semester
header  = []
header.append("Dept./Prog. (name)")
header.append("Course Code")
header.append("Course Name")
ty , td = sy , sd
while 1:
    header.append(str(ty)+"-"+(['Fall','Spring','Summer'][td-1]))
    td+=1
    if(ty==ey and td==ed+1):
        break
    if(td==4):
        td=1
        ty+=1
header.append("Total Offerings")
print(*header, sep = ", ") 
for i in range(codecnt):
    solveDep(codes[i],Names[i],sy,sd,ey,ed)
