import json

student = [
    {
        "student_id": 111,
        "first_name": "Brian",
        "last_name": "Hsu",
        "course_name": "CMPE273"
    },
    {
        "student_id": 112,
        "first_name": "Andy",
        "last_name": "Lu",
        "course_name": "CMPE273"
    }
]

classes = [
    {
        "class_id": 273,
        "course_name": "CMPE273",
        "students": [
        {
            "student_id": 111,
            "first_name": "Brian",
            "last_name": "Hsu",
            "course_name": "CMPE273"
        }
        ]
    }
]


def get_student(_, info, student_id):
    studs = [stu for stu in student if stu["student_id"] == int(student_id)]    
    return studs[0]

def get_class(_, info, class_id):
    clas = [clas for clas in classes if clas["class_id"] == int(class_id)]    
    return clas[0]

def create_student(_, info, student_id, first_name, last_name, course_name):
    global student
    student.append({'student_id' : student_id, 'first_name': first_name, 'last_name': last_name, 'course_name':course_name})
    return student

def create_class(_, info, class_id, course_name, student_id):
    global classes
    studs = [stu for stu in student if stu["student_id"] == int(student_id)]    
    classes.append({"class_id":class_id, "course_name":course_name, "students": studs})
    return classes

def add_student_to_class(_, info, class_id, student_id):
    global classes
    i = 0
    studs = [stu for stu in student if stu["student_id"] == int(student_id)]
    for j in classes:
        i = i+1
        if j["class_id"] == int(class_id):
            clas = j
            break
    clas["students"].append(studs[0])
    return clas