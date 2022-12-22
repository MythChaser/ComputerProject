import mysql.connector
import json
from matplotlib import pyplot
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "batch")
cursorObject = mydb.cursor()

def createBatch(batch_name):
    batch_id = batch_name[:3] + batch_name[6:8]
    department_name = batch_id[:3]
    print("Enter courses in batch: ")
    courses_L = []
    while(True):
        course = input("Enter course ID (to stop enter STOP): ")
        if(course.upper() == "STOP"):
            break
        else:
            courses_L.append(course)
    temp = ":"
    courses = (temp.join(courses_L))
    mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "student")
    cursorObject1 = mydb1.cursor()
    cursorObject1.execute("SELECT * FROM student")
    result1 = cursorObject1.fetchall()
    student_ids = []
    batch_ids = []
    for i in range(0, len(result1)):
        student_ids.append(result1[i][0])
        batch_ids.append(result1[i][3])
    student_id_L = []
    for i in range(0, len(batch_ids)):
        if(batch_ids[i] == batch_id):
            student_id_L.append(student_ids[i])
    student_id = (temp.join(student_id_L))
    sql = "INSERT INTO batch (batch_id, batch_name, department_name, list_of_courses, list_of_students) VALUES (%s, %s, %s, %s, %s)"
    val = (batch_id, batch_name, department_name, courses, student_id)
    cursorObject.execute(sql, val)
    mydb.commit()

def viewStudents(batch_id):
    cursorObject.execute("SELECT * FROM batch")
    result = cursorObject.fetchall()
    student_ids = []
    batch_ids = []
    for i in range(0, len(result)):
        student_ids.append(result[i][4])
        batch_ids.append(result[i][0])
    check = 0
    for i in range(0, len(batch_ids)):
        if(batch_ids[i] == batch_id):
            check = 1
            student_id = list(student_ids[i].split(":"))
            print("Students in batch: ")
            for j in student_id:
                print(j)
    if(check == 0):
        print("Batch does not exist")

def viewCourses(batch_id):
    cursorObject.execute("SELECT * FROM batch")
    result = cursorObject.fetchall()
    course_ids = []
    batch_ids = []
    for i in range(0, len(result)):
        course_ids.append(result[i][3])
        batch_ids.append(result[i][0])
    check = 0
    for i in range(0, len(batch_ids)):
        if(batch_ids[i] == batch_id):
            check = 1
            course_id = list(course_ids[i].split(":"))
            print("Courses in batch: ")
            for j in course_id:
                print(j)
    if(check == 0):
        print("Batch does not exist")

def viewPerformance(batch_id):
    cursorObject.execute("SELECT * FROM batch")
    result = cursorObject.fetchall()
    student_ids = []
    batch_ids = []
    for i in range(0, len(result)):
        student_ids.append(result[i][4])
        batch_ids.append(result[i][0])
    check = 0
    for i in range(0, len(batch_ids)):
        if(batch_ids[i] == batch_id):
            check = 1
            student_id = list(student_ids[i].split(":"))
            mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "student")
            cursorObject1 = mydb1.cursor()
            cursorObject1.execute("SELECT * FROM student")
            result1 = cursorObject1.fetchall()
            student_ids1 = []
            students = []
            student_rolls = []
            for j in range(0, len(result1)):
                student_ids1.append(result1[j][0])
                students.append(result1[j][1])
                student_rolls.append(result1[j][2])
            student_datas = [student_ids1, students, student_rolls]
            for j in range(0, len(student_id)):
                for k in range(0, len(student_ids1)):
                    if(student_id[j] == student_ids1[k]):
                        print("Student ID: " + student_datas[0][k])
                        print("Student Name: " + student_datas[1][k])
                        print("Student Roll Number: " + str(student_datas[2][k]))
                        mydb2 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
                        cursorObject2 = mydb2.cursor()
                        cursorObject2.execute("SELECT * FROM course")
                        result2 = cursorObject2.fetchall()
                        marks = []
                        subjects = []
                        for l in range(0, len(result2)):
                            marks.append(json.loads(result2[l][2]))
                            subjects.append(result2[l][1])
                        total_marks = 0
                        divs = 0
                        for l in range(0, len(subjects)):
                            temp = marks[l]
                            if(isinstance(temp.get(student_datas[0][k]), int)):
                                divs += 1
                                total_marks += temp.get(student_datas[0][k])
                        percentage = total_marks/divs
                        print("Percentage obtained: " + str(percentage))
                        print()
    if(check == 0):
        print("Batch does not exist")

def pieChart(batch_id):
    cursorObject.execute("SELECT * FROM batch")
    result = cursorObject.fetchall()
    student_ids = []
    batch_ids = []
    percentages = [">=90", ">=80", ">=70", ">=60", ">=50", "Failed"]
    numbers = [0, 0, 0, 0, 0, 0]
    for i in range(0, len(result)):
        student_ids.append(result[i][4])
        batch_ids.append(result[i][0])
    check = 0
    for i in range(0, len(batch_ids)):
        if(batch_ids[i] == batch_id):
            check = 1
            student_id = list(student_ids[i].split(":"))
            mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "student")
            cursorObject1 = mydb1.cursor()
            cursorObject1.execute("SELECT * FROM student")
            result1 = cursorObject1.fetchall()
            student_ids1 = []
            for j in range(0, len(result1)):
                student_ids1.append(result1[j][0])
            for j in range(0, len(student_id)):
                for k in range(0, len(student_ids1)):
                    if(student_id[j] == student_ids1[k]):
                        mydb2 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
                        cursorObject2 = mydb2.cursor()
                        cursorObject2.execute("SELECT * FROM course")
                        result2 = cursorObject2.fetchall()
                        marks = []
                        subjects = []
                        for i in range(0, len(result2)):
                            marks.append(json.loads(result2[i][2]))
                            subjects.append(result2[i][1])
                        total_marks = 0
                        divs = 0
                        for l in range(0, len(subjects)):
                            temp = marks[l]
                            if(isinstance(temp.get(student_ids1[k]), int)):
                                divs += 1
                                total_marks += temp.get(student_ids1[k])
                        percentage = total_marks/divs
                        if(percentage >= 90):
                            numbers[0] += 1
                        elif(percentage >= 80):
                            numbers[1] += 1
                        elif(percentage >= 70):
                            numbers[2] += 1
                        elif(percentage >= 60):
                            numbers[3] += 1
                        elif(percentage >= 50):
                            numbers[4] += 1
                        else:
                            numbers[5] += 1
            for i in range(len(numbers) - 1, -1, -1):
                if(numbers[i] == 0):
                    del numbers[i]
                    del percentages[i]
            fig = pyplot.figure(figsize =(10, 7))
            pyplot.pie(numbers, labels = percentages)
            pyplot.show()
    if(check == 0):
        print("Batch does not exist")
