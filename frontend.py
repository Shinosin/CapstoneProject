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
- id: int
- name: str
'''
def view_student(data:dict, message="") -> None:
    # display data
    return render_template('view.html',
                           entity="student",
                          data=data,
                          message=message)

#class
'''
A form for students to view existing classes.

Arguments:
- id: int
- name: str
- level: str
'''
def view_class(data:dict, message="") -> None:
    # display data
    return render_template('view.html',
                           entity="class",
                          data=data,
                          message=message)

#cca
'''
A form for students to add and view a cca.

Arguments:
- id: int
- name: str
'''
def add_cca(message="") -> None:
    return render_template(
        "add_cca.html",
        page_type="new",
        form_meta={
            "action": "/add_cca?confirm",
            "method": "POST"
        },
        form_data={
            "name": ""
        },
    message=message)
    
def confirm_cca(name:str) -> None:
    return render_template(
        "add_cca.html",
        page_type="confirm",
        form_meta={
            "action": "/add_cca?verify",
            "method": "POST"
        },
        form_data={
            "name": name 
        })


def view_cca(data:dict, message="") -> None:
    return render_template('view.html',
                           entity="cca",
                          data=data,
                          message=message)

#activity
'''
A form for students to add an activity.

Arguments:
- id: int
- start_date: int
- end_date: int
- activity_desc: str
'''
def add_activity(message="") -> None:
    return render_template(
            "add_activity.html",
            page_type="new",
            form_meta={
                "action": "/add_activity?confirm",
                "method": "POST"
            },
            form_data={
                "start_date": "",
                "end_date": "",
                "activity_desc": ""
            },
    message=message)

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

# membership - student-cca
'''
A form for students to enter a student id and cca id, to add a student into a cca.

Arguments:
- student_id: int
- cca_id: int
- role: str
'''
def edit_membership(names: list, message="") -> None:
    if "add" in request.args:
        return render_template(
            "student_cca.html",
            page_type="new",
            form_meta={
                "action": "/edit_membership?confirm",
                "method": "POST",
            },
            form_data={
                "student_id": "",
                "cca_id": "",
                "role": ""
            },
        message=message)
        
    elif "edit" in request.args:
        return render_template(
            "student_cca.html",
            page_type="edit",
            form_meta={
                "action": "/edit_membership?confirm",
                "method": "POST",
            },
            form_data={
                "student_id": "",
                "cca_id": "",
                "role": ""
            },
        message=message)
        
    else:
        return render_template(
            "edit_index.html",
            entity_rs="membership",
            entity1="student",
            entity2="a CCA",
            form_meta={
            "method": "GET"
        })

def confirm_membership(data:dict) -> None:
    return render_template(
        "student_cca.html",
        page_type="confirm",
        form_meta={
            "action": "/edit_membership?verify",
            "method": "POST"
        },
        form_data=data
    )

# participation - student-activity
'''
A form for students to enter a student id and activity id, to add a student into an activity

Arguments:
- student_id: int
- activity_id: str
- category: str
- role: str
- award: str
- hours: str
- coordinator: str
'''
def edit_participation(activity_ids: list, message="") -> None:
    if "add" in request.args:
        return render_template(
            "student_activity.html",
            page_type="new",
            form_meta={
                "action": "/edit_participation?confirm",
                "method": "POST",
            },
            form_data={
                "student_id": "",
                "activity_id": ""
            },
        message=message)
        
    elif "edit" in request.args:
        return render_template(
            "student_activity.html",
            page_type="edit",
            form_meta={
                "action": "/edit_participation?confirm",
                "method": "POST",
            },
            form_data={
                "student_id": "",
                "activity_id": ""
            },
        message=message)
        
    else:
        return render_template(
            "edit_index.html",
            entity_rs="participation",
            entity1="student",
            entity2="an activity",
            form_meta={
            "method": "GET"
        })

def confirm_participation(data:dict) -> None:
    return render_template(
        "student_activity.html",
        page_type="confirm",
        form_meta={
            "action": "/edit_participation?verify",
            "method": "POST"
        },
        form_data=data
    )