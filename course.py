import mysql.connector
import json
import pandas
import matplotlib.pyplot
from collections import Counter
from student import gradeCheck
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
cursorObject = mydb.cursor()

def createCourse(course_id, course_name):
    print("Enter students in course: ")
    marks_obtained_D = {}
    while(True):
        student_id = input("Enter student ID (to stop enter STOP): ")
        if(student_id.upper() == "STOP"):
            break
        else:
            marks = int(input("Enter marks obtained in course: "))
            marks_obtained_D[student_id] = marks
    marks_obtained = json.dumps(marks_obtained_D)
    sql = "INSERT INTO course (course_id, course_name, marks_obtained) VALUES (%s, %s, %s)"
    val = (course_id, course_name, marks_obtained)
    cursorObject.execute(sql, val)
    mydb.commit()

def checkPerformance(course_id):
    cursorObject.execute("SELECT * FROM course")
    myresult = cursorObject.fetchall()
    check = 0
    data = []
    for i in range(0, len(myresult)):
        if(myresult[i][0] == course_id):
            check = 1
            student_marks_d = json.loads(myresult[i][2])
            student_marks = [(k, v) for k, v in student_marks_d.items()]
            mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "student")
            cursorObject1 = mydb1.cursor()
            cursorObject1.execute("SELECT * FROM student")
            result = cursorObject1.fetchall()
            student_ids = []
            students = []
            student_rolls = []
            for j in range(0, len(result)):
                student_ids.append(result[j][0])
                students.append(result[j][1])
                student_rolls.append(result[j][2])
            student_datas = [student_ids, students, student_rolls]
            for j in range(0, len(student_marks)):
                for k in range(0, len(student_datas[0])):
                    if(student_marks[j][0] == student_datas[0][k]):
                        print("Student ID: " + student_datas[0][k])
                        print("Student Name: " + student_datas[1][k])
                        print("Student Roll Number: " + str(student_datas[2][k]))
                        print("Marks obtained: " + str(student_marks[j][1]))
                        print()
                        data.append([student_datas[0][k],student_datas[1][k],student_datas[1][k],student_datas[2][k],student_marks[j][1]])
    if(check == 0):
        print("Course does not exist")
    return data

def courseStatistics(course_id):
    mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "student")
    cursorObject1 = mydb1.cursor()
    cursorObject1.execute("SELECT * FROM student")
    result = cursorObject1.fetchall()
    student_ids = []
    for i in range(0, len(result)):
        student_ids.append(result[i][0])
    cursorObject.execute("SELECT * FROM course")
    result = cursorObject.fetchall()
    marks = []
    course_ids = []
    for i in range(0, len(result)):
        marks.append(json.loads(result[i][2]))
        course_ids.append(result[i][0])
    grades = []
    for i in range(0, len(student_ids)):
        x = None
        for j in range(0, len(course_ids)):
            temp = marks[j]
            if(isinstance(temp.get(student_ids[i]), int)):
                if(course_ids[j] == course_id):
                    x = temp.get(student_ids[i])
        if(isinstance(x, int)):
            grades.append(gradeCheck(x))
    if(len(grades) == 0):
        print("Course does not exist")
    else:
        grades.sort()
        letter_counts = Counter(grades)
        df = pandas.DataFrame.from_dict(letter_counts, orient='index')
        df.plot(kind='bar')
        matplotlib.pyplot.show()
