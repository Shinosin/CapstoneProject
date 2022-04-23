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
        cca_name = request.form["cca_name"] # str
        return frontend.confirm_cca(cca_name) # cca_name: str
    elif 'verify' in request.args: # check with database
        cca_name = request.form.to_dict() # dict
        if storage.database['cca'].insert(cca_name): # successfully inserted
            return frontend.redirect(cca_name) # cca_name: dict
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
        data = request.form.to_dict() # dict
        return frontend.confirm_activity(data)
    elif 'verify' in request.args:
        data = request.form.to_dict() # dict
        if storage.database['activity'].insert(data): # successfully inserted
            return frontend.redirect(data) # data: dict
        else:
            return frontend.add_activity(message='Failed to add Activity, Activity already exists.')
            
    else:
        return frontend.add_activity()

@app.route('/view_student', methods=['POST', 'GET'])
def view_student():
    if request.method == 'POST':
        data = storage.database['students'].get_all()
        return frontend.view_student(data)
    # I WANT DATA SHIN IN DICTIONARY FORM THANK

@app.route('/view_class', methods=['POST', 'GET'])
def view_class():
    return frontend.view_class()

@app.route('/view_cca', methods=['POST', 'GET'])
def view_cca():
    return frontend.view_cca()

@app.route('/view_activity', methods=['POST', 'GET'])
def view_activity():
    return frontend.view_activity()

@app.route('/redirect', methods=['POST'])
def redirect():
    data = request.form.to_dict()
    return frontend.redirect(data)

# Future Functions
@app.route('/login', methods=['GET'])
def login():
    return 'Not Implemented for Now.'

@app.route('/profile', methods=['GET'])
def profile():
    return 'Not Implemented for Now.'

if __name__ == "__main__":
    app.run('0.0.0.0')
