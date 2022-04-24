from flask import render_template

def splash():
    return render_template('splash.html')

def index(message=''):
    return render_template('index.html',
                           message=message)

def redirect(data:dict) -> None:
    return render_template('redirect.html',
                          form_data=data)

#student
'''
A form for students to view existing students.

Arguments:
- cca_id: int
- cca_name: str
'''
def view_student(data:dict) -> None:
    # display data
    return render_template('view.html',
                           entity="student",
                          data=data)

#class
'''
A form for students to view existing classes.

Arguments:
- class_id: int
- class_name: str
- class_level: str
'''
def view_class(data:dict) -> None:
    # display data
    return render_template('view.html',
                           entity="class",
                          data=data)

#cca
'''
A form for students to add and view a cca.

Arguments:
- cca_id: int
- cca_name: str
'''
def add_cca(message='') -> None:
    return render_template(
        "add_cca.html",
        page_type="new",
        form_meta={
            "action": "/add_cca?confirm",
            "method": "POST"
        },
        form_data={
            "cca_name": ""
        },
        message=message
    )
    
def confirm_cca(cca_name:str) -> None:
    return render_template(
        "add_cca.html",
        page_type="confirm",
        form_meta={
            "action": "/add_cca?verify",
            "method": "POST"
        },
        form_data={
            "name": cca_name 
        })

def view_cca(data:dict) -> None:
    return render_template('view.html',
                           entity="cca",
                          data=data)

#activity
'''
A form for students to add an activity.

Arguments:
- activity_id: int
- activity_startdate: int
- activity_enddate: int
- activity_desc: str
'''
def add_activity() -> None:
    return render_template(
            "add_activity.html",
            page_type="new",
            form_meta={
                "action": "/add_activity?confirm",
                "method": "POST"
            },
            form_data={
                "activity_date": "",
                "activity_desc": ""
            })

def confirm_activity(data:dict) -> None:
    return render_template(
        "add_activity.html",
        page_type="confirm",
        form_meta={
            "action": "/add_activity?verify",
            "method": "POST"
        },
        form_data=data
    )

def view_activity(data:dict) -> None:
    return render_template('view.html',
                           entity="activity",
                          data=data)    

# membership - student-cca
'''
A form for students to enter a student name and cca name, to add a student into a cca.

Arguments:
- student_id: int
- student_name: str
- cca_name: str (dropdown)
'''


# participation - student-activity
'''
A form for students to enter a student name and activity name, to add a student into an activity

Arguments:
- student_id: int
- student_name: str
- activity_name: str (dropdown)
'''