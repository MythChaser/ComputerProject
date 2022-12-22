import mysql.connector
from matplotlib import pyplot

def enterMarks(course_id):
    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
    cursorObject = mydb.cursor()
    cursorObject.execute("SELECT * FROM course")
    myresult = cursorObject.fetchall()
    course_name = ""
    check = 0
    marks = {}
    for i in range(0, len(myresult)):
        if(myresult[i][0] == course_id):
            course_name = myresult[i][1]
            check = 1
    if(check == 0):
        return marks
    else:
        print("Course name: " + course_name)
        mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "batch")
        cursorObject1 = mydb1.cursor()
        cursorObject1.execute("SELECT * FROM batch")
        myresult1 = cursorObject1.fetchall()
        for i in range(0, len(myresult1)):
            courses = list(myresult1[i][3].split(":"))
            for j in range(0, len(courses)):
                if(courses[j] == course_id):
                    students = list(myresult1[i][4].split(":"))
                    for k in students:
                        marks_obtained = int(input("Enter marks obtained by " + k + ": "))
                        marks[k] = marks_obtained
    return marks

def viewPerformanceE(course_id):
    marks = enterMarks(course_id)
    if(len(marks) == 0):
        print("Course does not exist / No students enrolled in course")
    else:
        print("Marks obtained: ")
        for key, value in marks.items():
            print(key + ": ", value)

def scatterPlot():
    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
    cursorObject = mydb.cursor()
    cursorObject.execute("SELECT * FROM course")
    myresult = cursorObject.fetchall()
    courses = []
    for i in range(0, len(myresult)):
        courses.append(myresult[i][0])
    mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "batch")
    cursorObject1 = mydb1.cursor()
    cursorObject1.execute("SELECT * FROM batch")
    myresult1 = cursorObject1.fetchall()
    batches = []
    performance = []
    for i in range(0, len(myresult1)):
        batches.append(myresult1[i][0])
        performance.append(0)
    for i in range(0, len(courses)):
        marks = enterMarks(courses[i])
        keys = list(marks.keys())
        values = list(marks.values())
        for j in range(0, len(batches)):
            a = 0
            b = 0
            for k in range(0, len(keys)):
                x = keys[k]
                if(batches[j] == x[:5]):
                    a += values[k]
                    b += 1
            if(isinstance(b, int) and b != 0):
                performance[j] = a/b
        pyplot.scatter(batches, performance)
    pyplot.show()
