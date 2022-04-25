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
        print(data)
        if data == []:
            return frontend.view(entity='student', data=data, message='Student {} cannot be found.'.format(search_value))
        
        else:
            return frontend.view(entity='student', data=data, message="Viewing Students with {} {}.".format(search_key, search_value))
    else: # all data
        data = storage.database['students'].get_all() # list of dict
        return frontend.view(entity='student', data=data, message='Viewing All Students.')

@app.route('/view_class', methods=['POST', 'GET'])
def view_class():
    if request.method == 'POST': # selected data
        search_key = request.form['search_key']
        search_value = request.form['search_value']
        record = {search_key: search_value} # dict
        data = storage.database['classes'].find(record) # list of dict
        
        if data == []:
            return frontend.view(entity='class', data=data, message='Class {} cannot be found.'.format(search_value))
        
        else:
            return frontend.view(entity='class', data=data, message="Viewing Classes with {} {}.".format(search_key, search_value))
    else: # all data
        data = storage.database['classes'].get_all() # list of dict
        return frontend.view(entity='class', data=data, message='Viewing All Classes.')

@app.route('/view_cca', methods=['POST', 'GET'])
def view_cca():
    if request.method == 'POST': # selected data
        search_key = request.form['search_key']
        search_value = request.form['search_value']
        record = {search_key: search_value} # dict
        data = storage.database['ccas'].find(record) # list of dict
        
        if data == []:
            return frontend.view(entity='cca', data=data, message='CCA {} cannot be found.'.format(search_value))
        
        else:
            return frontend.view(entity='cca', data=data, message="Viewing CCAs with {} {}.".format(search_key, search_value))
    else: # all data
        data = storage.database['ccas'].get_all() # list of dict
        return frontend.view(entity='cca', data=data, message='Viewing All CCAs.')

@app.route('/view_activity', methods=['POST', 'GET'])
def view_activity():
    if request.method == 'POST': # selected data
        search_key = request.form['search_key']
        search_value = request.form['search_value']
        record = {search_key: search_value} # dict
        data = storage.database['activities'].find(record) # list of dict
        
        if data == []:
            return frontend.view(entity='activity', data=data, message='Activity {} cannot be found.'.format(search_value))
        
        else:
            return frontend.view(entity='activity', data=data, message="Viewing Activities with {} {}.".format(search_key, search_value))
            
    else: # all data
        data = storage.database['activities'].get_all() # list of dict
        print(data)
        return frontend.view(entity='activity', data=data, message='Viewing All Activities.')

@app.route('/view_subject', methods=['POST'])
def view_subject():
    student_id = request.form['id']
    record = {'student_id': student_id}
    student_name = storage.database['students'].find(
        {'id': student_id },
        column='name'
    )
    data = storage.database['subject'].find(record)
    return frontend.view(entity='subject', data=data)

@app.route('/edit_membership', methods=['POST', 'GET'])
def edit_membership():
    return frontend.edit_membership()

@app.route('/edit_participation', methods=['POST', 'GET'])
def edit_participation():
    return frontend.edit_partipcipation()
        
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
