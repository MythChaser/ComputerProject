import mysql.connector
import json
from matplotlib import pyplot
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "department")
cursorObject = mydb.cursor()

def createDepartment(department_id, department_name):
    mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "batch")
    cursorObject1 = mydb1.cursor()
    cursorObject1.execute("SELECT * FROM batch")
    result1 = cursorObject1.fetchall()
    batch_ids = []
    department_names = []
    for i in range(0, len(result1)):
        department_names.append(result1[i][2])
        batch_ids.append(result1[i][0])
    batch_id_L = []
    for i in range(0, len(department_names)):
        if(department_names[i] == department_id):
            batch_id_L.append(batch_ids[i])
    temp = ":"
    batch_id = (temp.join(batch_id_L))
    sql = "INSERT INTO department (department_id, department_name, list_of_batches) VALUES (%s, %s, %s)"
    val = (department_id, department_name, batch_id)
    cursorObject.execute(sql, val)
    mydb.commit()

def viewBatches(department_id):
    cursorObject.execute("SELECT * FROM department")
    result = cursorObject.fetchall()
    batch_ids = []
    department_ids = []
    for i in range(0, len(result)):
        batch_ids.append(result[i][2])
        department_ids.append(result[i][0])
    check = 0
    for i in range(0, len(department_ids)):
        if(department_ids[i] == department_id):
            check = 1
            batch_id = list(batch_ids[i].split(":"))
            print("Batches in course: ")
            for j in batch_id:
                print(j)
    if(check == 0):
        print("Department does not exist")

def viewPerformanceD(department_id):
    cursorObject.execute("SELECT * FROM department")
    result = cursorObject.fetchall()
    department_ids = []
    batches = []
    for i in range(0, len(result)):
        department_ids.append(result[i][0])
        batches.append(result[i][2])
    check = 0
    for i in range(0, len(department_ids)):
        if(department_ids[i] == department_id):
            check = 1
            total_percentage1 = 0
            divs2 = 0
            batch_id_L = list(batches[i].split(":"))
            for j in range(0, len(batch_id_L)):
                batch_id = batch_id_L[j]
                total_percentage = 0
                divs1 = 0
                mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "batch")
                cursorObject1 = mydb1.cursor()
                cursorObject1.execute("SELECT * FROM batch")
                result1 = cursorObject1.fetchall()
                student_ids = []
                batch_ids = []
                for k in range(0, len(result1)):
                    student_ids.append(result1[k][4])
                    batch_ids.append(result1[k][0])
                for k in range(0, len(batch_ids)):
                    if(batch_ids[k] == batch_id):
                        student_id = list(student_ids[k].split(":"))
                        mydb2 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "student")
                        cursorObject2 = mydb2.cursor()
                        cursorObject2.execute("SELECT * FROM student")
                        result2 = cursorObject2.fetchall()
                        student_ids1 = []
                        for l in range(0, len(result2)):
                            student_ids1.append(result2[l][0])
                        for l in range(0, len(student_id)):
                            for m in range(0, len(student_ids1)):
                                if(student_id[l] == student_ids1[m]):
                                    mydb3 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
                                    cursorObject3 = mydb3.cursor()
                                    cursorObject3.execute("SELECT * FROM course")
                                    result3 = cursorObject3.fetchall()
                                    marks = []
                                    subjects = []
                                    for n in range(0, len(result3)):
                                        marks.append(json.loads(result3[n][2]))
                                        subjects.append(result3[n][1])
                                    total_marks = 0
                                    divs = 0
                                    for n in range(0, len(subjects)):
                                        temp = marks[n]
                                        if(isinstance(temp.get(student_ids1[m]), int)):
                                            divs += 1
                                            total_marks += temp.get(student_ids1[m])
                                    if(isinstance(divs, int) and divs != 0):
                                        percentage = total_marks/divs
                                        total_percentage += percentage
                                        divs1 += 1
                        if(isinstance(divs1, int) and divs1 != 0):
                            batch_percentage = total_percentage/divs1
                            total_percentage1 += batch_percentage
                            divs2 += 1
            if(isinstance(divs2, int) and divs2 != 0):
                print("Average percentage of all batches: " + str(total_percentage1/divs2))
    if(check == 0):
        print("Department does not exist")

def linePlot(department_id):
    cursorObject.execute("SELECT * FROM department")
    result = cursorObject.fetchall()
    department_ids = []
    batches = []
    for i in range(0, len(result)):
        department_ids.append(result[i][0])
        batches.append(result[i][2])
    check = 0
    for i in range(0, len(department_ids)):
        if(department_ids[i] == department_id):
            check = 1
            batch_name = []
            percentages = []
            batch_id_L = list(batches[i].split(":"))
            for j in range(0, len(batch_id_L)):
                batch_id = batch_id_L[j]
                total_percentage = 0
                divs1 = 0
                mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "batch")
                cursorObject1 = mydb1.cursor()
                cursorObject1.execute("SELECT * FROM batch")
                result1 = cursorObject1.fetchall()
                student_ids = []
                batch_ids = []
                for k in range(0, len(result1)):
                    student_ids.append(result1[k][4])
                    batch_ids.append(result1[k][0])
                for k in range(0, len(batch_ids)):
                    if(batch_ids[k] == batch_id):
                        student_id = list(student_ids[k].split(":"))
                        mydb2 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "student")
                        cursorObject2 = mydb2.cursor()
                        cursorObject2.execute("SELECT * FROM student")
                        result2 = cursorObject2.fetchall()
                        student_ids1 = []
                        for l in range(0, len(result2)):
                            student_ids1.append(result2[l][0])
                        for l in range(0, len(student_id)):
                            for m in range(0, len(student_ids1)):
                                if(student_id[l] == student_ids1[m]):
                                    mydb3 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
                                    cursorObject3 = mydb3.cursor()
                                    cursorObject3.execute("SELECT * FROM course")
                                    result3 = cursorObject3.fetchall()
                                    marks = []
                                    subjects = []
                                    for n in range(0, len(result3)):
                                        marks.append(json.loads(result3[n][2]))
                                        subjects.append(result3[n][1])
                                    total_marks = 0
                                    divs = 0
                                    for n in range(0, len(subjects)):
                                        temp = marks[n]
                                        if(isinstance(temp.get(student_ids1[m]), int)):
                                            divs += 1
                                            total_marks += temp.get(student_ids1[m])
                                    if(isinstance(divs, int) and divs != 0):
                                        percentage = total_marks/divs
                                        total_percentage += percentage
                                        divs1 += 1
                        if(isinstance(divs1, int) and divs1 != 0):
                            batch_percentage = total_percentage/divs1
                        else:
                            batch_percentage = 0
                        batch_name.append(batch_id)
                        percentages.append(batch_percentage)
            if(len(percentages) != 0):
                pyplot.plot(batch_name, percentages)
                pyplot.show()  
    if(check == 0):
        print("Department does not exist")
