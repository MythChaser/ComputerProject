import mysql.connector
import json
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "student")
cursorObject = mydb.cursor()

def createStudent(student_id, name):
    class_roll_number = int(student_id[5:7])
    batch_id = student_id[:5]
    sql = "INSERT INTO student (student_id, name, class_roll_number, batch_id) VALUES (%s, %s, %s, %s)"
    val = (student_id, name, class_roll_number, batch_id)
    cursorObject.execute(sql, val)
    mydb.commit()

def updateStudent(ostudent_id, nstudent_id, name):
    class_roll_number = int(nstudent_id[5:7])
    batch_id = nstudent_id[0:5]
    sql = "UPDATE student SET student_id = %s, name = %s, class_roll_number = %s, batch_id = %s WHERE student_id = %s"
    val = (nstudent_id, name, class_roll_number, batch_id, ostudent_id)
    cursorObject.execute(sql, val)
    mydb.commit()

def removeStudent(student_id):
    sql = "DELETE FROM student WHERE student_id = %s"
    val = (student_id, )
    cursorObject.execute(sql, val)
    mydb.commit()

def reportCard(student_idx):
    cursorObject.execute("SELECT * FROM student")
    result = cursorObject.fetchall()
    students = []
    student_ids = []
    for i in range(0, len(result)):
        student_ids.append(result[i][0])
        students.append(result[i][1])
    check = 0
    for i in range(0, len(student_ids)):
        if(student_idx == student_ids[i]):
            check = 1
            break
    if(check == 1):
        studentx = students[i]
        mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
        cursorObject1 = mydb1.cursor()
        cursorObject1.execute("SELECT * FROM course")
        result = cursorObject1.fetchall()
        marks = []
        subjects = []
        for i in range(0, len(result)):
            marks.append(json.loads(result[i][2]))
            subjects.append(result[i][1])
        file_name = student_idx + ".txt"
        file = open(file_name, "w+")
        student_id = "Student ID: " + student_idx + " \n"
        name = "Name: " + studentx + " \n"
        L = [student_id, name]
        file.writelines(L)
        total_marks = 0
        divs = 0
        for i in range(0, len(subjects)):
            temp = marks[i]
            if(isinstance(temp.get(student_idx), int)):
                subject_marks = "Marks in " + subjects[i] + ": " + str(temp.get(student_idx)) + "% \n"
                divs += 1
                total_marks += temp.get(student_idx)
                file.write(subject_marks)
        grade = "Grade obtained: " + gradeCheck(total_marks/divs) + " \n"
        file.write(grade)
        file.close()
    else:
        print("Student ID does not exist")

def gradeCheck(a):
    if(a >= 90):
        return "A"
    elif(a >= 80):
        return "B"
    elif(a >= 70):
        return "C"
    elif(a >= 60):
        return "D"
    elif(a >= 50):
        return "E"
    else:
        return "F"
