import json
import csv
import pandas
from batch import createBatch

def createStudent(student_id, name):
    class_roll_number = int(student_id[5:7])
    batch_id = student_id[:5]
    data = [student_id, name, class_roll_number, batch_id]
    csv_reader = []
    with open("student.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    with open("student.csv", "a", newline = "\n") as f:
        for i in range(0, len(csv_reader)):
            if(csv_reader[i][0] == student_id):
                print("Student ID already exists")
                return
        csv_writer = csv.writer(f)
        csv_writer.writerow(data)
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == batch_id):
            check = 1
            if(csv_reader[i][4] == ""):
                csv_reader[i][4] = csv_reader[i][4] + student_id
            else:
                csv_reader[i][4] = csv_reader[i][4] + ":" + student_id
            df = pandas.read_csv("batch.csv")
            df.loc[i-1, "list_of_students"] = csv_reader[i][4]
            df.to_csv("batch.csv", index = False)
    if(check == 0):
        print("Batch does not exist.... Creating new batch")
        batch_name = batch_id[:3] + " 20" + batch_id[3:] + "-" + str(int(batch_id[3:]) + 4)
        createBatch(batch_name)
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    courses = []
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == batch_id):
            courses = list(csv_reader[i][3].split(":"))
    with open("course.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    for i in range(0, len(csv_reader)):
        for j in range(0, len(courses)):
            if(csv_reader[i][0] == courses[j]):
                if(csv_reader[i][2] == ""):
                    temp = {}
                    temp[student_id] = 0
                    csv_reader[i][2] = json.dumps(temp)
                else:
                    temp = json.loads(csv_reader[i][2])
                    temp[student_id] = 0
                    csv_reader[i][2] = json.dumps(temp)
                df = pandas.read_csv("course.csv")
                df.loc[i-1, "marks_obtained"] = csv_reader[i][2]
                df.to_csv("course.csv", index = False)

def updateStudent(ostudent_id):
    csv_reader = []
    with open("student.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == ostudent_id):
            check = 1
            break
    if(check == 0):
        print("Student ID does not exist")
        return
    while(True):
        print("Press 1 to update name")
        print("Press 2 to update student ID")
        print("Press 0 to exit")
        x = int(input("Enter your choice: "))
        if(x == 0):
            break
        elif(x == 1):
            name = input("Enter updated name: ")
            df = pandas.read_csv("student.csv")
            df.loc[i-1, "Name"] = name
            df.to_csv("student.csv", index = False)
        elif(x == 2):
            nstudent_id = input("Enter updated student ID: ")
            df = pandas.read_csv("student.csv")
            df.loc[i-1, "Student_ID"] = nstudent_id
            df.to_csv("student.csv", index = False)
            removeStudent(ostudent_id)
            createStudent(nstudent_id, csv_reader[i][1])
            ostudent_id = nstudent_id
            with open("student.csv", "r", newline = "\n") as f:
                csv_reader = list(csv.reader(f, delimiter=","))
        else:
            print("Invalid input. Try again.")

def removeStudent(student_id):
    csv_reader = []
    with open("student.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == student_id):
            check = 1
            break
    if(check == 0):
        print("Student ID does not exist")
        return
    df = pandas.read_csv("student.csv")
    df.set_index("Student_ID")
    df = df.drop(df.index[i-1])
    df.to_csv("student.csv", index = False)
    with open("course.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    for i in range(0, len(csv_reader)):
        if(i == 0):
            continue
        temp = csv_reader[i][2]
        temp = json.loads(temp)
        if student_id in temp:
            del temp[student_id]
        csv_reader[i][2] = json.dumps(temp)
    df = pandas.read_csv("course.csv")
    for i in range(1, len(csv_reader)):
        df.loc[i-1, "marks_obtained"] = csv_reader[i][2]
    df.to_csv("course.csv", index = False)
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    for i in range(0, len(csv_reader)):
        if(i == 0):
            continue
        temp = list(csv_reader[i][4].split(":"))
        if student_id in temp:
            temp.remove(student_id)
        a = ":"
        csv_reader[i][4] = a.join(temp)
    df = pandas.read_csv("batch.csv")
    for i in range(1, len(csv_reader)):
        df.loc[i-1, "list_of_students"] = csv_reader[i][4]
    df.to_csv("batch.csv", index = False)

def reportCard(student_id):
    name = ""
    csv_reader= []
    with open("student.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == student_id):
            check = 1
            name = csv_reader[i][1]
            break
    if(check == 0):
        print("Student ID does not exist")
        return
    f = open((student_id + ".txt"), "w")
    a = "Student ID: " + student_id + "\n"
    b = "Name: " + name + "\n"
    f.writelines([a, b])
    with open("course.csv", "r", newline = "\n") as fx:
        csv_reader = list(csv.reader(fx, delimiter=","))
    marks = []
    subjects = []
    for i in range(1, len(csv_reader)):
        marks.append(json.loads(csv_reader[i][2]))
        subjects.append(csv_reader[i][1])
    total_marks = 0
    divs = 0
    for i in range(0, len(subjects)):
        temp = marks[i]
        if(isinstance(temp.get(student_id), int)):
            subject_marks = "Marks in " + subjects[i] + ": " + str(temp.get(student_id)) + "% \n"
            divs += 1
            total_marks += temp.get(student_id)
            f.write(subject_marks)
    grade = "Grade obtained: " + gradeCheck(total_marks/divs) + " \n"
    f.write(grade)
    f.close()

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
