import csv
import pandas
import json
from matplotlib import pyplot
from department import createDepartment

def createBatch(batch_name):
    batch_id = batch_name[:3] + batch_name[6:8]
    department_id = batch_id[:3]
    csv_reader = []
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == batch_id):
            print("Batch ID already exists")
            return
    data = [batch_id, batch_name, department_id, "", ""]
    with open("batch.csv", "a", newline = "\n") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(data)
    print("Enter courses in batch: ")
    while(True):
        course_id = input("Enter course ID (to stop enter STOP): ")
        with open("batch.csv", "r", newline = "\n") as f:
            csv_reader = list(csv.reader(f, delimiter=","))
        if(csv_reader[len(csv_reader) - 1][3] != ""):
            check = 0
            temp = csv_reader[len(csv_reader) - 1][3].split(":")
            for x in temp:
                if(x == course_id):
                    print("Course already added")
                    check = 1
            if(check == 1):
                continue
        if(course_id.upper() == "STOP"):
            break
        else:
            with open("course.csv", "r", newline = "\n") as f:
                csv_reader = list(csv.reader(f, delimiter=","))
            check = 0
            for i in range(0, len(csv_reader)):
                if(csv_reader[i][0] == course_id):
                    with open("batch.csv", "r", newline = "\n") as f:
                        csv_reader = list(csv.reader(f, delimiter=","))
                    check = 1
                    if(csv_reader[len(csv_reader) - 1][3] == ""):
                        csv_reader[len(csv_reader) - 1][3] = csv_reader[len(csv_reader) - 1][3] + course_id
                    else:
                        csv_reader[len(csv_reader) - 1][3] = csv_reader[len(csv_reader) - 1][3] + ":" + course_id
                    df = pandas.read_csv("batch.csv")
                    df.loc[len(csv_reader) - 2, "list_of_courses"] = csv_reader[len(csv_reader) - 1][3]
                    df.to_csv("batch.csv", index = False)
            if(check == 0):
                print("Course does not exist. Please create course first.")
    with open("department.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == department_id):
            check = 1
            if(csv_reader[i][2] == ""):
                csv_reader[i][2] = csv_reader[i][2] + batch_id
            else:
                csv_reader[i][2] = csv_reader[i][2] + ":" + batch_id
            df = pandas.read_csv("department.csv")
            df.loc[i-1, "list_of_batches"] = csv_reader[i][2]
            df.to_csv("department.csv", index = False)
    if(check == 0):
        print("Department does not exist.... Creating new department")
        department_name = input("Enter department name: ")
        createDepartment(department_id, department_name)
        with open("department.csv", "r", newline = "\n") as f:
            csv_reader = list(csv.reader(f, delimiter=","))
        csv_reader[len(csv_reader) - 1][2] = csv_reader[len(csv_reader) - 1][2] + batch_id
        df = pandas.read_csv("department.csv")
        df.loc[len(csv_reader) - 2, "list_of_batches"] = csv_reader[len(csv_reader) - 1][2]
        df.to_csv("department.csv", index = False)

def viewStudents(batch_id):
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    students = []
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == batch_id):
            check = 1
            students = csv_reader[i][4].split(":")
            break
    if(check == 0):
        print("Batch ID does not exist")
        return
    print("Students in " + batch_id + ":")
    for student in students:
        print(student)

def viewCourses(batch_id):
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    courses = []
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == batch_id):
            check = 1
            courses = csv_reader[i][3].split(":")
            break
    if(check == 0):
        print("Batch ID does not exist")
        return
    print("Courses in " + batch_id + ":")
    for course in courses:
        print(course)

def viewPerformance(batch_id):
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    students = []
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == batch_id):
            check = 1
            students = csv_reader[i][4].split(":")
            break
    if(check == 0):
        print("Batch ID does not exist")
        return
    for student in students:
        with open("student.csv", "r", newline = "\n") as f:
            csv_reader = list(csv.reader(f, delimiter=","))
        for i in range(0, len(csv_reader)):
            if(student == csv_reader[i][0]):
                print("Student ID: " + student)
                print("Student Name: " + csv_reader[i][1])
                print("Student Roll Number: " + csv_reader[i][2])
        with open("course.csv", "r", newline = "\n") as f:
            csv_reader = list(csv.reader(f, delimiter=","))
        all_marks = []
        for i in range(1, len(csv_reader)):
            all_marks.append(json.loads(csv_reader[i][2]))
        total_marks = 0
        divs = 0
        for subjects in all_marks:
            if(isinstance(subjects.get(student), int)):
                total_marks += subjects.get(student)
                divs += 1
        print("Percentage obtained: " + str(total_marks/divs))
        print()


def pieChart(batch_id):
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    students = []
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == batch_id):
            check = 1
            students = csv_reader[i][4].split(":")
            break
    if(check == 0):
        print("Batch ID does not exist")
        return
    percentages = [">=90", ">=80", ">=70", ">=60", ">=50", "Failed"]
    numbers = [0, 0, 0, 0, 0, 0]
    for student in students:
        with open("course.csv", "r", newline = "\n") as f:
            csv_reader = list(csv.reader(f, delimiter=","))
        all_marks = []
        for i in range(1, len(csv_reader)):
            all_marks.append(json.loads(csv_reader[i][2]))
        total_marks = 0
        divs = 0
        for subjects in all_marks:
            if(isinstance(subjects.get(student), int)):
                total_marks += subjects.get(student)
                divs += 1
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
    pyplot.pie(numbers, labels = percentages)
    pyplot.show()
