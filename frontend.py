from flask import render_template

def splash():
    return render_template('splash.html')

def index(message=''):
    return render_template('index.html',
                           message=message)

'''
Redirects to a success (confirmation) page
'''
def redirect(data:dict) -> None:
    return render_template('redirect.html',
                          form_data=data)

# view function
'''
A form to view data
'''
def view(entity, data:dict, message="") -> None:
    return render_template("view.html",
                          entity=entity,
                          data=data,
                          message=message)

# add functions
# cca
'''
A form for students to add a cca.

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

# activity
'''
A form for students to add an activity.

Arguments:
- id: int
- start_date: int
- end_date: int
- description: str
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
                "description": ""
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
def add_membership(names: list, message="") -> None:
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
            "role": "Member"
        },
    message=message)
    
def edit_membership(names: list, message="") -> None:
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
- activity_id: int
- category: str
- role: str
- award: str
- hours: int
- coordinator: str
'''
def add_participation(activity_ids: list, message="") -> None:
    return render_template(
        "student_activity.html",
        page_type="new",
        form_meta={
            "action": "/edit_participation?confirm",
            "method": "POST",
        },
        form_data={
            "student_id": "",
            "activity_id": "",
            "category": "",
            "role": "Participant",
            "award": "",
            "hours": "",
            "coordinator": ""
        },
    message=message)
        
def edit_participation(activity_ids: list, message="") -> None:
    return render_template(
        "student_activity.html",
        page_type="edit",
        form_meta={
            "action": "/edit_participation?confirm",
            "method": "POST",
        },
        form_data={
            "student_id": "",
            "activity_id": "",
            "category": "",
            "role": "Participant",
            "award": "",
            "hours": "",
            "coordinator": ""
        },
    message=message)

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