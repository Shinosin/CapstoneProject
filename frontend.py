from flask import render_template

def splash():
    return render_template('splash.html')

def index(message=''):
    return render_template('index.html',
                           message=message)

def redirect(data):
    return render_template('redirect.html',
                          form_data=data)

#student and class
def view_student(data):
    # display data
    return render_template('view.html',
                           entity="student",
                          data=data)

#cca
def add_cca():
    return render_template(
        "add_cca.html",
        page_type="new",
        form_meta={
            "action": "/add_cca?confirm",
            "method": "POST"
        },
        form_data={
            "cca_name": ""
        })
    
def confirm_cca(cca_name):
    return render_template(
        "add_cca.html",
        page_type="confirm",
        form_meta={
            "action": "/redirect",
            "method": "POST"
        },
        form_data={
            "cca_name": cca_name 
        })

def view_cca(data):
    return render_template('view.html',
                           entity="cca",
                          data=data)

#activity
def add_activity():
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

def confirm_activity(data):
    return render_template(
        "add_activity.html",
        page_type="confirm",
        form_meta={
            "action": "/redirect",
            "method": "POST"
        },
        form_data=data
    )

def view_activity(data):
    return render_template('view.html',
                           entity="activity",
                          data=data)    

# membership - student-cca
'''
A form for students to enter a student name and cca name, to add a student into a cca.

Arguments:
- student_name: str
- cca_name: str (dropdown)
'''


# participation - student-activity
'''
A form for students to enter a student name and activity name, to add a student into an activity

Arguments:
- student_name: str
- activity_name: str (dropdown)
'''