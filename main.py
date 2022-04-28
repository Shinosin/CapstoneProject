from flask import Flask, request
import frontend
import storage

app = Flask(__name__)

@app.route('/')
def splash():
    """Welcome Page
    Access to: /login and /index.
    """
    return frontend.splash()

@app.route('/index', methods=['POST','GET'])
def index():
    """Index Page. User actions are displayed.
    Access to: /add_cca, /add_activity, /profile,
               /view_student, /view_class, /view_cca, /view_activity
               /edit_membership, /edit_participation.
    """
    return frontend.index()

@app.route('/add_cca', methods=['POST', 'GET'])
def add_cca():
    """Creating a new club
    1. New Form for students to fill in new club data (club name)
    2. Confirmation page for students to ensure the details are correct
    3. Verify with database if Club name already exists
    """
    if "confirm" in request.args: # confirmation page
        cca_name = request.form["name"] # str
        return frontend.confirm_cca(cca_name) # cca_name: str
    elif 'verify' in request.args: # check with database
        cca_name = request.form.to_dict() # dict
        if storage.database['ccas'].insert(cca_name): # successfully inserted
            data = {}
            data['cca_name'] = cca_name['name'] # for display
            return frontend.redirect(data) # data: dict
        else:
            return frontend.add_cca(message='Failed to add CCA, CCA already exists.')
    else:
        return frontend.add_cca()

@app.route('/add_activity', methods=['POST', 'GET'])
def add_activity():
    """Creating a new activity
    1. New Form for students to fill in new activity data
    2. Confirmation page for students to ensure the details are correct
    3. Verify with database if Activity name already exists
    """
    if 'confirm' in request.args:
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        data = request.form.to_dict() # dict

        # verifying date format
        if storage.database['activities'].validate_date(start_date): # check valid date format
            if end_date != "": # they have input end date
                if storage.database['activities'].validate_date(end_date): # check valid date format
                    return frontend.confirm_activity(data)
            else:
                return frontend.confirm_activity(data)
        else:
            return frontend.add_activity(message='Start Date and End Date should be in YYYYMMDD format.')
    elif 'verify' in request.args:
        data = request.form.to_dict() # dict
        if storage.database['activities'].insert(data): # successfully inserted
            return frontend.redirect(data) # data: dict
        else:
            return frontend.add_activity(message='Failed to add Activity, Activity already exists.')
            
    else:
        return frontend.add_activity()

@app.route('/view_student', methods=['POST', 'GET'])
def view_student():
    if request.method == 'POST': # selected data
        search_key = request.form['search_key']
        search_value = request.form['search_value']
        record = {search_key: search_value} # dict
        data = storage.database['students'].find(record) # list of dict
        if data == []:
            return frontend.view_student(data=data, message='Student {} {} cannot be found.'.format(search_key, search_value))
        
        else:
            return frontend.view_student(data=data, message="Viewing Students with {} {}.".format(search_key, search_value))
    else: # all data
        data = storage.database['students'].get_all() # list of dict
        return frontend.view_student(data=data, message='Viewing All Students.')

@app.route('/view_class', methods=['POST', 'GET'])
def view_class():
    if request.method == 'POST': # selected data
        search_key = request.form['search_key']
        search_value = request.form['search_value']
        record = {search_key: search_value} # dict
        data = storage.database['classes'].find(record) # list of dict
        
        if data == []:
            return frontend.view_class(data=data, message='Class {} {} cannot be found.'.format(search_key, search_value))
        
        else:
            return frontend.view_class(data=data, message="Viewing Classes with {} {}.".format(search_key, search_value))
    else: # all data
        data = storage.database['classes'].get_all() # list of dict
        return frontend.view_class(data=data, message='Viewing All Classes.')

@app.route('/view_cca', methods=['POST', 'GET'])
def view_cca():
    if request.method == 'POST': # selected data
        search_key = request.form['search_key']
        search_value = request.form['search_value']
        record = {search_key: search_value} # dict
        data = storage.database['ccas'].find(record) # list of dict
        
        if data == []:
            return frontend.view_cca(data=data, message='CCA {} {} cannot be found.'.format(search_key, search_value))
        
        else:
            return frontend.view_cca(data=data, message="Viewing CCAs with {} {}.".format(search_key, search_value))
    else: # all data
        data = storage.database['ccas'].get_all() # list of dict
        return frontend.view_cca(data=data, message='Viewing All CCAs.')

@app.route('/view_activity', methods=['POST', 'GET'])
def view_activity():
    if request.method == 'POST': # selected data
        search_key = request.form['search_key']
        search_value = request.form['search_value']
        record = {search_key: search_value} # dict
        data = storage.database['activities'].find(record) # list of dict
        
        if data == []:
            return frontend.view_activity(data=data, message='Activity {} {} cannot be found.'.format(search_key, search_value))
        
        else:
            return frontend.view_activity(data=data, message="Viewing Activities with {} {}.".format(search_key, search_value))
            
    else: # all data
        data = storage.database['activities'].get_all() # list of dict
        print(data)
        return frontend.view_activity(data=data, message='Viewing All Activities.')

@app.route('/view_subject', methods=['POST'])
def view_subject():
    student_id = request.form['id']
    record = {'student_id': student_id}
    student_name = storage.database['students'].find(
        {'id': student_id },
        column='name'
    ) # list of dict
    list_of_subject_code = storage.database['student_subject'].find(record, column='subject_code')
    data = []
    for record in list_of_subject_code:
        data.extend(storage.database['subjects'].find(record))
    return frontend.view_subject(student_name=student_name[0]['name'], data=data)


@app.route('/add_membership', methods=['POST', 'GET'])
def add_membership():
    """Modify Membership
    1. Select a cca name from the list of cca names
    2. display table of existing members in cca
    3. display table of the rest of the students
    4. choose students to be added
    5. from the selected students -> give confirmation page
    
    1. get cca_name from form (give)
    2. list of student name and class name (give) who are not in cca (cca id)
    3. and list who are in cca student name and class name

    Create confirm form
    1. get list of student name and class (give)

    1. add to database (student id: list of int, ccaid: int)
    1a. convert student name to student id
    2. send data again to say yay u added (redirect)
    """
    if request.method == 'GET':
        cca_name = storage.database['ccas'].get_all(column='name') # list of dict
        return frontend.cca_membership(action="add", cca_names=cca_name)

    elif 'choose' in request.args:
        cca_name = request.form['cca_name']
        cca_id = storage.database['ccas'].find({'name': cca_name}, column='id') # list of dict
        existing_members = storage.database['student_cca'].existing_members(cca_id[0]['id'])
        not_in_cca = storage.database['student_cca'].not_in_cca(cca_id[0]['id'])
        return frontend.choose_membership(in_cca=existing_members, out_cca=not_in_cca , cca_name=cca_name)

    elif 'confirm' in request.args:
        cca_name = request.form['cca_name']
        student_id = request.form.getlist('choose')
        data = []
        for id in student_id:
            data.extend(
                storage.database['students'].find(
                    {'id': id}, column='id, name')
            )
        for record in data:
            print(record)
        return frontend.confirm_membership(action='add', data=data, cca_name=cca_name)

    elif 'verify' in request.args:
        cca_name = request.form['cca_name']
        # student_name = request.form.getlist('name')
        # student_class = request.form.getlist('class')
        student_id = request.form.getlist('choose')
        data = []
        for id in student_id:
            student = storage.database['students'].find({'id': id}, column='id, name')
            data.extend(student)
        return frontend.data_membership(data, cca_name)

@app.route('/edit_membership', methods=['POST', 'GET'])
def edit_membership():
    pass
        
                
        



# @app.route('/edit_membership', methods=['POST', 'GET'])
# def edit_membership():
#     if 'verify' in request.args: # Step 4: Modify Database
#         student_id = request.form.getlist('id') # student_id is a list
#         cca_name = request.form['name']
#         cca_id = storage.database['ccas'].find(
#             {"name": cca_name},
#             column='id'
#         )
#         cca_id = cca_id[0]
#         storage.database['ccas'].insert_member(student_id=student_id
#                                            cca_id=cca_id[0]) # insert into database
#         return frontend.success_membership(message="Successfully edited membership of {}".format(cca_name))

#     elif 'confirm' in request.args: # Step 3: Confirm
#         ClubName = request.form['ClubName']
#         student_id = request.form.getlist('StudentID') # student_id is a list
#         student_data = []
#         for id in student_id:
#             student = storage.coll['student'].find(column='ID, Name', ID=id)
#             student_data.extend(student)
#         return frontend.membership_confirm(club_name=ClubName,
#                                            student_data=student_data)







@app.route('/add_participation', methods=['POST', 'GET'])
def edit_participation():
    return frontend.participation()







    

    
# Future Functions
@app.route('/login', methods=['GET'])
def login():
    return 'Not Implemented for Now.'

@app.route('/logout', methods=['GET'])
def logout():
    """Return user to welcome page"""
    return frontend.splash()

@app.route('/profile', methods=['GET'])
def profile():
    return 'Not Implemented for Now.'

if __name__ == "__main__":
    app.run('0.0.0.0')
