import json
import csv
import pandas
import matplotlib.pyplot
from collections import Counter
from student import gradeCheck
from batch import createBatch

def createCourse(course_id, course_name):
    csv_reader = []
    with open("course.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == course_id):
            print("Course ID already exists")
            return
    print("Enter batches in which course is included: ")
    students = []
    while(True):
        batch_id = input("Enter batch ID (to stop enter STOP): ")
        if(batch_id.upper() == "STOP"):
            break
        else:
            check = 0
            for i in range(0, len(csv_reader)):
                with open("batch.csv", "r", newline = "\n") as f:
                    csv_reader = list(csv.reader(f, delimiter=","))
                if(csv_reader[i][3] != ""):
                    temp = csv_reader[i][3].split(":")
                    for x in temp:
                        if(x == course_id):
                            print("Course already added")
                            continue
                if(csv_reader[i][0] == batch_id):
                    check = 1
                    if(csv_reader[i][3] == ""):
                        csv_reader[i][3] = csv_reader[i][3] + course_id
                    else:
                        csv_reader[i][3] = csv_reader[i][3] + ":" + course_id
                    df = pandas.read_csv("batch.csv")
                    df.loc[i-1, "list_of_courses"] = csv_reader[i][3]
                    df.to_csv("batch.csv", index = False)
            if(check == 0):
                print("Batch does not exist.... Creating new batch")
                batch_name = batch_id[:3] + " 20" + batch_id[3:] + "-" + str(int(batch_id[3:]) + 4)
                createBatch(batch_name)
                with open("batch.csv", "r", newline = "\n") as f:
                    csv_reader = list(csv.reader(f, delimiter=","))
                csv_reader[len(csv_reader) - 1][3] = csv_reader[len(csv_reader) - 1][3] + course_id
                df = pandas.read_csv("batch.csv")
                df.loc[len(csv_reader) - 2, "list_of_courses"] = csv_reader[len(csv_reader) - 1][3]
                df.to_csv("batch.csv", index = False)
            with open("batch.csv", "r", newline = "\n") as f:
                csv_reader = list(csv.reader(f, delimiter=","))
            for i in range(0, len(csv_reader)):
                if(csv_reader[i][0] == batch_id):
                    students += csv_reader[i][4].split(":")
    temp = {}
    for a in students:
        temp[a] = 0
    data = [course_id, course_name, json.dumps(temp)]
    with open("course.csv", "a", newline = "\n") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(data)

def checkPerformance(course_id):
    csv_reader = []
    data = []
    with open("course.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    student_marks = {}
    for i in range(1, len(csv_reader)):
        if(csv_reader[i][0] == course_id):
            check = 1
            student_marks = json.loads(csv_reader[i][2])
            break
    if(check == 0):
        print("Course ID does not exist")
        return data
    student_ids = list(student_marks.keys())
    with open("student.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    for i in range(0, len(student_ids)):
        for j in range(0, len(csv_reader)):
            if(student_ids[i] == csv_reader[j][0]):
                print("Student ID: " + student_ids[i])
                print("Student Name: " + csv_reader[j][1])
                print("Student Roll Number: " + csv_reader[j][2])
                print("Marks obtained: " + str(student_marks.get(student_ids[i])))
                print()
                data.append([student_ids[i], csv_reader[j][1], csv_reader[j][2], student_marks.get(student_ids[i])])
    return data

def courseStatistics(course_id):
    csv_reader = []
    with open("course.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == course_id):
            check = 1
            break
    if(check == 0):
        print("Course ID does not exist")
        return
    x = checkPerformance(course_id)
    grades = []
    for a in x:
        grades.append(gradeCheck(a[3]))
    grades.sort()
    letter_counts = Counter(grades)
    df = pandas.DataFrame.from_dict(letter_counts, orient='index')
    df.plot(kind='bar')
    matplotlib.pyplot.show()
