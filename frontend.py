from flask import render_template

def splash():
    return render_template('splash.html')

def index():
    return render_template('index.html')

def redirect(data: dict, form, name=None, action="change") -> None:
    '''Redirects to a success (confirmation) page'''
    return render_template('redirect.html',
                          form_data=data,
                           form=form,
                           action=action,
                          name=name)

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
                           entity="students",
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
                           entity="classes",
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
                           entity="ccas",
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
                           entity="activities",
                           headers=[
                               {"label": "Activity ID", "value": "id"},
                               {"label": "Activity Name", "value": "name"},
                               {"label": "Activity Start Date", "value": "start_date"},
                               {"label": "Activity End Date", "value": "end_date"},
                               {"label": "Activity Description", "value": "description"},
                               {"label": "Coordinator", "value": "coordinator"}],
                           data=data,
                           message=message)

"""
A form to view subject data

Arguments:
- subject_code: str
- name: str
- level: str
"""
def view_subject(data: list, student_name: dict) -> None:
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
                "action": "/membership/add?choose",
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
            "action": "/view/membership",
            "method": "GET",
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
        "action": "/membership/add?confirm",
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
            {"label": "Student Class", "value": "class"},
            {"label": "Role", "value": "role"}
        ],
        message=message
    )

def edit_membership(data: dict, cca_name) -> None:
    # data: student_name & class_name
    return render_template(
        "student_cca.html",
        page_type="edit",
        form_meta={
            "action": "/membership/edit?verify",
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
                "action_yes": "/membership/add?verify",
                "action_no": "/membership/add",
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
                "action_yes": "/membership/edit?verify",
                "action_no": "/view/membership",
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
                "action_yes": "/membership/delete?verify",
                "action_no": "/view/membership",
                "method": "POST"
            },
            form_data=data,
            action=action,
            cca_name=cca_name
        )

# participation - student-activity
'''
A form for students to select an activity and students, to add a student into an activity

Arguments:
- student_id: int
- activity_id: int
- activity_name: str
- category: str
- role: str
- award: str
- hours: int
- coordinator: int

- activity_names: list of dicts
- in_activity: list of dicts
- out_activity: list of dicts
- message: str
'''
def activity_participation(action, activity_names: list, message="") -> None:
    # action: add / edit
    if action == "add":
        return render_template(
            "student_activity.html",
            page_type="activity",
            form_meta={
                "action": "/participation/add?choose",
                "method": "POST",
            },
            form_data={
                "activity_name": ""
            },
            activity_names=activity_names,
            message=message
        )
    elif action == "edit":
        return render_template(
        "student_activity.html",
        page_type="activity",
        form_meta={
            "action": "/view/participation",
            "method": "GET",
        },
        form_data={
            "activity_name": ""
        },
        activity_names=activity_names,
        message=message
    )

def choose_participation(out_activity: list, in_activity: list, activity_name: str, message="") -> None:
    return render_template(
        "student_activity.html",
        page_type="add",
    form_meta={
        "action": "/participation/add?confirm",
        "method": "POST"
    },
        activity_name=activity_name,
        out_activity=out_activity,
        in_activity=in_activity,
        headers=[
            {"label": "Student Name", "value": "name"},
            {"label": "Student Class", "value": "class"}
        ],
        message=message
    )
   
def view_participation(in_activity: list, activity_name, message="") -> None:
    return render_template(
        "student_activity.html",
        page_type="view",
        activity_name=activity_name,
        in_activity=in_activity,
        headers=[
            {"label": "Student Name", "value": "name"},
            {"label": "Student Class", "value": "class"},
            {"label": "Coordinator", "value": "coordinator"},
            {"label": "Category", "value": "category"},
            {"label": "Role", "value": "role"},
            {"label": "Award", "value": "award"},
            {"label": "Hours", "value": "hours"}
        ],
        message=message
    )

def edit_participation(data: dict, activity_name) -> None:
    # data: student_name & class_name
    return render_template(
        "student_activity.html",
        page_type="edit",
        form_meta={
            "action": "/participation/edit?verify",
            "method": "POST"
        },
        form_data=data,
        activity_name=activity_name
    )

def confirm_participation(action, data: list, activity_name) -> None:
    # action: add / edit / delete
    # data: student_name, class_name, things that were changed
    if action == "add":
        return render_template(
            "student_activity.html",
            page_type="confirm",
            form_meta={
                "action_yes": "/participation/add?verify",
                "action_no": "/participation/add",
                "method": "POST"
            },
            form_data=data,
            action=action,
            activity_name=activity_name
        )

    elif action == "edit":
        return render_template(
            "student_activity.html",
            page_type="confirm",
            form_meta={
                "action_yes": "/participation/edit?verify",
                "action_no": "/view/participation",
                "method": "POST"
            },
            form_data=data,
            action=action,
            activity_name=activity_name
        )

    elif action == "delete":
        return render_template(
            "student_activity.html",
            page_type="confirm",
            form_meta={
                "action_yes": "/participation/delete?verify",
                "action_no": "/view/participation",
                "method": "POST"
            },
            form_data=data,
            action=action,
            activity_name=activity_name
        )