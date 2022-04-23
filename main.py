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
    """Index Page. User actions are displayed
    Access to: /add_cca, /add_activity, /profile,
               /view_student, /view_class, /view_cca, /view_activity
               /edit_membership, /edit_participation
    """
    return frontend.index()

@app.route('/add_cca', methods=['POST', 'GET'])
def add_cca():
    if "confirm" in request.args: # confirmation page
        cca_name = request.form["cca_name"]
        return frontend.confirm_cca(cca_name)
    else:
        return frontend.add_cca()

@app.route('/add_activity', methods=['POST', 'GET'])
def add_activity():
    if 'confirm' in request.args:
        data = dict(request.form)
        return frontend.confirm_activity(data)
    else:
        return frontend.add_activity()

@app.route('/view_student', methods=['POST', 'GET'])
def view_student():
    return frontend.view_student()
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
