from flask import render_template

def splash():
    return render_template('splash.html')

def index(message=''):
    return render_template('index.html',
                           message=message)

'''
Redirects to a success (confirmation) page
'''
def redirect(data: dict) -> None:
    return render_template('redirect.html',
                          form_data=data)

# view functions
'''
A form to view student data.

Arguments:
- id: int
- name: str
- student_class: int
- age: int
- year_enrolled: int
- graduating_year: int
'''
def view_student(data: list, message="") -> None:
    return render_template("view.html",
                          entity="student",
                           headers=[
                               {"label": "Student ID", "value": "id"},
                               {"label": "Student Name", "value": "name"},
                               {"label": "Student Class", "value": "student_class"},
                               {"label": "Student Age", "value": "age"},
                               {"label": "Year Enrolled", "value": "year_enrolled"},
                               {"label": "Graduating Year", "value": "graduating_year"}],
                          data=data,
                          message=message)

'''
A form to view class data.

Arguments:
- id: int
- name: str
- level: str
'''
def view_class(data: list, message="") -> None:
    return render_template("view.html",
                          entity="class",
                           headers=[
                               {"label": "Class ID", "value": "id"},
                               {"label": "Class Name", "value": "name"},
                               {"label": "Class Level", "value": "level"}],
                          data=data,
                          message=message)

'''
A form to view cca data.

Arguments:
- id: int
- name: str
'''
def view_cca(data: list, message="") -> None:
    return render_template("view.html",
                          entity="cca",
                           headers=[
                               {"label": "CCA ID", "value": "id"},
                               {"label": "CCA Name", "value": "name"}],
                          data=data,
                          message=message)

'''
A form to view activity data.

Arguments:
- id: int
- start_date: int
- end_date: int
- description: str
'''
def view_activity(data: list, message="") -> None:
    return render_template("view.html",
                          entity="activity",
                           headers=[
                               {"label": "Activity ID", "value": "id"},
                               {"label": "Activity Start Date", "value": "start_date"},
                               {"label": "Activity End Date", "value": "end_date"},
                               {"label": "Activity Description", "value": "description"}],
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

    
def confirm_cca(name: str) -> None:
    return render_template(
        "add_cca.html",
        page_type="confirm",
        form_meta={
            "action": "/add_cca?verify",
            "method": "POST"
        },
        form_data={
            "name": name
        },
        headers={
            "label": "CCA Name",
            "value": "name"
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

def confirm_activity(data: dict) -> None:
    return render_template(
        "add_activity.html",
        page_type="confirm",
        form_meta={
            "action": "/add_activity?verify",
            "method": "POST"
        },
        form_data=data,
    headers=[        
        {"label": "Activity Start Date",
        "name": "start_date"},
        {"label": "Activity End Date",
        "name": "end_date"},
        {"label": "Activity Description",
        "name": "description"}
    ])

# membership - student-cca
'''
A form for students to enter a student id and cca id, to add a student into a cca.

Arguments:
- student_id: int
- cca_id: int
- role: str
'''
def add_membership(student_ids: list, cca_ids: list, message="") -> None:
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
            "role": "MEMBER"
        },
        student_ids=student_ids,
        cca_ids=cca_ids,
        message=message)
    
def edit_membership(student_ids: list, cca_ids: list, message="") -> None:
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
        student_ids=student_ids,
        cca_ids=cca_ids,
        message=message)

def confirm_membership(data: dict) -> None:
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
- coordinator: int
'''
def add_participation(student_ids: list, activity_ids: list, message="") -> None:
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
        student_ids=student_ids,
        activity_ids=activity_ids,
        message=message)
        
def edit_participation(student_ids: list, activity_ids: list, message="") -> None:
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
        student_ids=student_ids,
        activity_ids=activity_ids,
        message=message)

def confirm_participation(data: dict) -> None:
    return render_template(
        "student_activity.html",
        page_type="confirm",
        form_meta={
            "action": "/edit_participation?verify",
            "method": "POST"
        },
        form_data=data
    )