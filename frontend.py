from flask import render_template

def splash():
    return render_template('splash.html')

def index():
    return render_template('index.html')

def redirect(data: dict, cca_name=None) -> None:
    '''Redirects to a success (confirmation) page'''
    return render_template('redirect.html',
                          form_data=data,
                          cca_name=cca_name)

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
                               {"label": "Student Age", "value": "age"},
                               {"label": "Year Enrolled", "value": "year_enrolled"},
                               {"label": "Graduating Year", "value": "graduating_year"},
                               {"label": "Student Class", "value": "student_class"}],     
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
                               {"label": "Activity Name", "value": "name"},
                               {"label": "Activity Start Date", "value": "start_date"},
                               {"label": "Activity End Date", "value": "end_date"},
                               {"label": "Activity Description", "value": "description"}],
                           data=data,
                           message=message)

"""
A form to view subject data

Arguments:
- subject_code: str
- name: str
- level: str
"""
def view_subject(data: list, student_name: str) -> None:
    return render_template("view.html",
                           entity="subject",
                           headers=[
                               {"label": "Subject Code", "value": "subject_code"},
                               {"label": "Subject Name", "value": "name"},
                               {"label": "Subject Level", "value": "level"}
                           ],
                           data=data,
                           student_name=student_name)
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
                "name": "",
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
        form_data=data)

# membership - student-cca
'''
A form for students to enter a student id and cca id, to add a student into a cca.

Arguments:
- student_id: int
- cca_id: int
- role: str
'''
def cca_membership(action, cca_names: list, message="") -> None:
    # action: add / edit
    if action == "add":
        return render_template(
            "student_cca.html",
            page_type="cca",
            form_meta={
                "action": "/add_membership?choose",
                "method": "POST",
            },
            form_data={
                "cca_name": ""
            },
            cca_names=cca_names,
            message=message
        )
    elif action == "edit":
        return render_template(
        "student_cca.html",
        page_type="cca",
        form_meta={
            "action": "/view_membership",
            "method": "POST",
        },
        form_data={
            "cca_name": ""
        },
        cca_names=cca_names,
        message=message
    )

def choose_membership(out_cca: list, in_cca: list, cca_name: str, message="") -> None:
    return render_template(
        "student_cca.html",
        page_type="add",
    form_meta={
        "action": "/add_membership?confirm",
        "method": "POST"
    },
        cca_name=cca_name,
        out_cca=out_cca,
        in_cca=in_cca,
        headers=[
            {"label": "Student Name", "value": "name"},
            {"label": "Student Class", "value": "class"}
        ],
        message=message
    )
   
def view_membership(in_cca: list, cca_name, message="") -> None:
    return render_template(
        "student_cca.html",
        page_type="view",
        cca_name=cca_name,
        in_cca=in_cca,
        headers=[
            {"label": "Student Name", "value": "name"},
            {"label": "Student Class", "value": "class"}
        ],
        message=message
    )

def edit_membership(data: dict, cca_name) -> None:
    # data: student_name & class_name
    return render_template(
        "student_cca.html",
        page_type="edit",
        form_meta={
            "action": "edit_membership?confirm",
            "method": "POST"
        },
        form_data=data,
        cca_name=cca_name
    )

def confirm_membership(action, data: list, cca_name) -> None:
    # action: add / edit / delete
    # data: student_name, class_name, things that were changed
    if action == "add":
        return render_template(
            "student_cca.html",
            page_type="confirm",
            form_meta={
                "action_yes": "/add_membership?verify",
                "action_no": "/add_membership",
                "method": "POST"
            },
            form_data=data,
            action=action,
            cca_name=cca_name
        )

    elif action == "edit":
        return render_template(
            "student_cca.html",
            page_type="confirm",
            form_meta={
                "action_yes": "/edit_membership?verify",
                "action_no": "/edit_membership",
                "method": "POST"
            },
            form_data=data,
            action=action,
            cca_name=cca_name
        )

    elif action == "delete":
        return render_template(
            "student_cca.html",
            page_type="confirm",
            form_meta={
                "action_yes": "/delete_membership?verify",
                "action_no": "/view_membership",
                "method": "POST"
            },
            form_data=data,
            action=action,
            cca_name=cca_name
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