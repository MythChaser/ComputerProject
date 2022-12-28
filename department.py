import json
import csv
from matplotlib import pyplot

def createDepartment(department_id, department_name):
    csv_reader = []
    with open("department.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == department_id):
            print("Department ID already exists")
            return
    data = [department_id, department_name, ""]
    with open("department.csv", "a", newline = "\n") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(data)

def viewBatches(department_id):
    with open("department.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    batches = []
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][0] == department_id):
            check = 1
            batches = csv_reader[i][2].split(":")
            break
    if(check == 0):
        print("Department ID does not exist")
        return
    print("Batches in " + department_id + ":")
    for batch in batches:
        print(batch)

def viewPerformanceD(department_id):
    with open("department.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    batches = []
    for i in range(1, len(csv_reader)):
        if(csv_reader[i][0] == department_id):
            check = 1
            batches = csv_reader[i][2].split(":")
            break
    if(check == 0):
        print("Department ID does not exist")
        return
    if(len(batches) == 0):
        print("No batches in department")
        return
    performances = []
    for batch in batches:
        students = []
        student_performances = []
        with open("batch.csv", "r", newline = "\n") as f:
            csv_reader = list(csv.reader(f, delimiter=","))
        for i in range(0, len(csv_reader)):
            if(csv_reader[i][0] == batch):
                students = csv_reader[i][4].split(":")
                break
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
            if(divs != 0):
                student_performances.append(total_marks/divs)
            else:
                student_performances.append(0)
        total_marks = 0
        divs = 0
        for x in student_performances:
            total_marks += x
            divs += 1
        if(divs != 0):
            performances.append(total_marks/divs)
        else:
            performances.append(0)
    total_marks = 0
    divs = 0
    for i in range(0, len(batches)):
        total_marks += performances[i]
        divs += 1
    avg_percentage = 0
    if(divs != 0):
        avg_percentage = total_marks/divs
    print("Average percantage obtained by all batches in " + department_id + ": " + str(avg_percentage))

def linePlot(department_id):
    with open("department.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    batches = []
    for i in range(1, len(csv_reader)):
        if(csv_reader[i][0] == department_id):
            check = 1
            batches = csv_reader[i][2].split(":")
            break
    if(check == 0):
        print("Department ID does not exist")
        return
    if(len(batches) == 0):
        print("No batches in department")
        return
    performances = []
    for batch in batches:
        students = []
        student_performances = []
        with open("batch.csv", "r", newline = "\n") as f:
            csv_reader = list(csv.reader(f, delimiter=","))
        for i in range(0, len(csv_reader)):
            if(csv_reader[i][0] == batch):
                students = csv_reader[i][4].split(":")
                break
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
            if(divs != 0):
                student_performances.append(total_marks/divs)
            else:
                student_performances.append(0)
        total_marks = 0
        divs = 0
        for x in student_performances:
            total_marks += x
            divs += 1
        if(divs != 0):
            performances.append(total_marks/divs)
        else:
            performances.append(0)
    pyplot.plot(batches, performances)
    pyplot.show()
