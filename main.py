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
               /view/students, /view/classes, /view/ccas, /view/activities
               /membership/add, /membership/edit,
               /participation/add, /participation/edit.
    """
    return frontend.index()

@app.route('/view/<form>', methods=['POST', 'GET'])
def view(form):
    '''Viewing different entities'''
    if request.method == 'POST': # filter functions for view page
        search_key = request.form['search_key'] # str
        search_value = request.form['search_value'] # str
        data = storage.database[form].find(
            {search_key: search_value}
        ) # list of dict
        
    if form == 'students':
        
        if request.method == 'POST': # filter
            
            if data == []:
                return frontend.view_student(
                    data=data,
                    message='Student {} {} cannot be found.'.format(search_key, search_value)
                )
            else:
                return frontend.view_student(
                    data=data,
                    message="Viewing Students with {} {}.".format(search_key, search_value)
                )
            
        else:
            data = storage.database[form].get_all() # list of dict
            return frontend.view_student(data=data, message='Viewing All Students.')

    elif form == 'classes':

        if request.method == 'POST': # filter
            
            if data == []:
                return frontend.view_class(
                    data=data,
                    message='Class {} {} cannot be found.'.format(search_key, search_value)
                )
            else:
                return frontend.view_class(
                    data=data,
                    message="Viewing Classes with {} {}.".format(search_key, search_value)
                )

        else:
            data = storage.database[form].get_all() # list of dict
            return frontend.view_class(data=data, message='Viewing All Classes.')

    elif form == 'ccas':

        if request.method == 'POST': # filter
            
            if data == []:
                return frontend.view_cca(
                    data=data,
                    message='CCA {} {} cannot be found.'.format(search_key, search_value)
                )
            else:
                return frontend.view_cca(
                    data=data,
                    message="Viewing CCAs with {} {}.".format(search_key, search_value)
                )

        else:
            data = storage.database[form].get_all() # list of dict
            return frontend.view_cca(data=data, message='Viewing All CCAs.')

    elif form == 'activities':

        if request.method == 'POST': # filter
             
            if data == []:
                return frontend.view_activity(
                    data=data,
                    message='Activity {} {} cannot be found.'.format(search_key, search_value)
                )
            else:
                return frontend.view_activity(
                    data=data,
                    message="Viewing Activities with {} {}.".format(search_key, search_value)
                )

        else:
            data = storage.database[form].get_all() # list of dict
            return frontend.view_activity(data=data, message='Viewing All Activities.')

    elif form == 'subject': # GET
        student_name = storage.database['students'].find(
            {'id': request.args['id'] },
            column='name'
        ) # list of dict
        subject_code = storage.database['student_subject'].find(
            {'student_id': request.args['id']},
            column='subject_code'
        ) # list of dict

        data = []
        for record in subject_code:
            data.extend(storage.database['subjects'].find(record))

        return frontend.view_subject(student_name=student_name[0], data=data)
    
    elif form == 'membership': # GET
 #########       # SELECT ROLE OSO
        
        cca_id = storage.database['ccas'].find(
            {'name': request.args['cca_name']},
            column='id'
        ) # list of dict
        existing_members = storage.database['student_cca'].display_membership(cca_id[0]['id']) # list of dict
        return frontend.view_membership(
            in_cca=existing_members,
            cca_name=request.args['cca_name']
        )

    elif form == 'participation': # GET
        activity_id = storage.database['activities'].find(
            {'name': request.args['activity_name']},
            column='id'
        ) # list of dict
        existing_participants = storage.database['student_activity'].existing_participants(
            activity_id[0]['id']
        )
        return frontend.view_participation(
            in_activity=existing_participants,
            activity_name=request.args['activity_name']
        )
        

@app.route('/add_cca', methods=['POST', 'GET'])
def add_cca():
    """Creating a new cca
    1. New Form for students to fill in new cca data (cca name)
    2. Confirmation page for students to ensure the details are correct
    3. Verify with database if CCA name already exists
    """
    if "confirm" in request.args: # confirmation page
        cca_name = request.form["name"] # str
        return frontend.confirm_cca(cca_name) # cca_name: str
        
    elif 'verify' in request.args: # check with database
        cca_name = request.form.to_dict() # dict
        
        if storage.database['ccas'].insert(cca_name): # successfully inserted
            data = {}
            data['cca_name'] = cca_name['name'] # for display
            return frontend.redirect([data]) # data: dict
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
            return frontend.redirect([data]) # data: dict
        else:
            return frontend.add_activity(message='Failed to add Activity, Activity already exists.')
            
    else:
        return frontend.add_activity()


@app.route('/membership/<action>', methods=['POST', 'GET'])
def membership(action):
    if action == 'add':
        """Modify Membership
        1. Select a cca name from the list of cca names
        2. Display table of existing members in cca
        3. Display table of the rest of the students
        4. Choose students to be added
        5. From the selected students -> give confirmation page
        6. Add into database
        7. Show success page
        """
        if request.method == 'POST':
            cca_name = request.form['cca_name']
            cca_id = storage.database['ccas'].find(
                {'name': request.form['cca_name']},
                column='id'
            ) # list of dict
            
        if request.method == 'GET':
            '''Form to choose cca which you want to add people into'''
            cca_name = storage.database['ccas'].get_all(column='name') # list of dict
            return frontend.cca_membership(action="add", cca_names=cca_name)

        elif 'choose' in request.args:
            '''
            Select students to add into the cca
            in_cca: List of records (dict) of students in the cca
            out_cca: List of records (dict) of students not in the cca
            '''
            existing_members = storage.database['student_cca'].existing_members(cca_id[0]['id'])
            not_in_cca = storage.database['student_cca'].not_in_cca(cca_id[0]['id'])
            return frontend.choose_membership(
                in_cca=existing_members,
                out_cca=not_in_cca,
                cca_name=cca_name
            )

        elif 'edit' in request.args:
            student_id = storage.database['students'].find(
                {'name': request.form['name']},
                column='id'
            )
            data = storage.database['student_cca'].select_by_student_id(student_id)
            return frontend.edit_membership(data, cca_name)
        
        elif 'confirm' in request.args:
            '''
            Display information for student to confirm
            student_name: List of student_names to be added into cca
            student_class: List of student_class who are to be added into cca
            '''
            student_id = request.form.getlist('choose')
            data = storage.database['student_cca'].select_by_student_id(student_id)
            return frontend.confirm_membership(action='add', data=data, cca_name=cca_name)
    
        elif 'verify' in request.args:
            '''
            Insert student(s) into database
            (student_id: list, cca_id: int)
            Display success page
            '''
            student_id = request.form.getlist('id')
            storage.database['student_cca'].add_members(
                student_id,
                cca_id[0]['id']
            )
            data = storage.database['student_cca'].select_by_student_id(student_id)
            return frontend.redirect(data, cca_name)

    elif action == 'edit' or action == 'delete':

        data = [{
                'name': request.form['name'],
                'class': request.form['class'] 
            }] # list of dict
        cca_name = request.form['cca_name'] # str
        cca_id = storage.database['ccas'].find(
                {'name': request.form['cca_name']},
                column='id'
            ) # list of dict
        student_id = storage.database['students'].find(
                {'name': request.form['name']},
                column='id'
            ) # list of dict

        if 'confirm' in request.args:
            '''Display confirmation page'''
            return frontend.confirm_membership(action, data, cca_name)
            
        elif 'verify' in request.args:
            '''Update role in database OR Delete record'''
            if action == 'edit':
                storage.database['student_cca'].update_role(
                    {'student_id': student_id[0]['id'],
                     'cca_id': cca_id[0]['id']},
                    role=request.form['role']
                )
                return frontend.redirect(data, cca_name, action)
            elif action == 'delete':
                storage.database['student_cca'].delete(
                {'student_id': student_id[0]['id'],
                 'cca_id': cca_id[0]['id']}
            )            
                return frontend.redirect(data, cca_name, action)

    elif action == 'display':
        '''Form to choose cca which you want to add people into'''
        cca_name = storage.database['ccas'].get_all(column='name') # list of dict
        return frontend.cca_membership(action="edit", cca_names=cca_name)





@app.route('/participation', methods=['POST', 'GET'])
def participation(action):
    if action == 'add':
        """Modify Participation
        1. Select a activity name from the list of activity names
        2. Display table of existing participants in activity
        3. Display table of the rest of the students
        4. Choose students to be added
        5. From the selected students -> give confirmation page
        6. Add into database
        7. Show success page
        """
        if request.method == 'POST':
            activity_name = request.form['activity_name']
            activity_id = storage.database['activities'].find(
                {'name': request.form['activity_name']},
                column='id'
            ) # list of dict
            
        if request.method == 'GET':
            '''Form to choose activity which you want to add people into'''
            activity_name = storage.database['activities'].get_all(column='name') # list of dict
            return frontend.cca_membership(action="add", activity_names=activity_name)

        elif 'choose' in request.args:
            '''
            Select students to add into the activity
            in_activity: List of records (dict) of students in the activity
            out_activity: List of records (dict) of students not in the activity
            '''
            existing_participants = storage.database['student_activity'].existing_participants(activity_id[0]['id'])
            not_in_activity = storage.database['student_activity'].not_in_activity(activity_id[0]['id'])
            return frontend.choose_participation(
                in_activity=existing_participants,
                out_activity=not_in_activity,
                activity_name=activity_name
            )
    
        elif 'confirm' in request.args:
            '''
            Display information for student to confirm
            student_name: List of student_names to be added into activity
            student_class: List of student_class who are to be added into activity
            '''
            student_id = request.form.getlist('choose')
            data = storage.database['student_activity'].select_by_student_id(student_id)
            return frontend.confirm_membership(action='add', data=data, activity_name=activity_name)
    
        elif 'verify' in request.args:
            '''
            Insert student(s) into database
            (student_id: list, activity_id: int)
            Display success page
            '''
            student_id = request.form.getlist('id')
            storage.database['student_activity'].add_participants(
                student_id,
                activity_id[0]['id']
            )
            data = storage.database['student_activity'].select_by_student_id(student_id)
            return frontend.redirect(data, activity_name)

    elif action == 'edit' or action == 'delete':

        data = [{
                'name': request.form['name'],
                'class': request.form['class'] 
            }] # list of dict
        activity_name = request.form['activity_name'] # str
        activity_id = storage.database['activities'].find(
                {'name': request.form['activity_name']},
                column='id'
            ) # list of dict
        student_id = storage.database['students'].find(
                {'name': request.form['name']},
                column='id'
            ) # list of dict

        if 'confirm' in request.args:
            '''Display confirmation page'''
            return frontend.confirm_membership(action, data, activity_name)
            
        elif 'verify' in request.args:
            '''Update ... in database OR Delete record'''
            if action == 'edit':
                storage.database['student_activity'].update_role(
                    {'student_id': student_id[0]['id'],
                     'activity_id': activity_id[0]['id']},
                    role=request.form['role']
                )
                return frontend.redirect(data, activity_name, action)
            elif action == 'delete':
                storage.database['student_activity'].delete(
                {'student_id': student_id[0]['id'],
                 'activity_id': activity_id[0]['id']}
            )
            
            return frontend.redirect(data, activity_name)

    elif action == 'display':
        '''Form to choose activity which you want to add people into'''
        activity_name = storage.database['activities'].get_all(column='name') # list of dict
        return frontend.activity_membership(action="edit", activity_names=activity_name)

    
# Future Functions


### FUTURE FUNCTIONS ### 
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