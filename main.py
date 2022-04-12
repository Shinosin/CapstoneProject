from flask import Flask, request
import frontend
import storage

app = Flask(__name__)

@app.route('/')
def splash():
    return frontend.splash()  # welcome page

@app.route('/index', methods=['POST','GET'])
def index():
    if request.method == 'POST': # redirect from successful submission
        data = request.form["name"]
        # can add to database here
        # figure out how to differentiate
        message = f'Successfully added {data}'
        return frontend.index(message)
    else:
        return frontend.index()

@app.route('/add_cca', methods=['POST', 'GET'])
def add_cca():
    if "confirm" in request.args: # confirmation page
        cca_name = request.form["name"]
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

@app.route('/view_class', methods=['POST', 'GET'])
def view_class():
    return frontend.view_class()

@app.route('/view_cca', methods=['POST', 'GET'])
def view_cca():
    return frontend.view_cca()

@app.route('/view_class', methods=['POST', 'GET'])
def view_activity():
    return frontend.view_activity()

@app.route('/display', methods=['GET','POST'])
def display(): # display found data in appropriate format
    search_key = request.form['search']
    if 'Student' in request.args:
    #     # search for student
    #     return frontend.display(# student info)
    # elif...
        return f'Student: {search_key}'
    elif 'Class' in request.args:
        return f'Class: {search_key}'
    else:
        return 'failed'

@app.route('/redirect', methods=['POST'])
def redirect():
    data = request.form
    return frontend.redirect(data)

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if helper.verify(username, password) == 0:
#             return frontend.index()
#         elif helper.verify(username, password) == 1:
#             return frontend.login('Wrong password.')
#         else:
#             return frontend.login('User does not exists.')
#     else:
#         return frontend.login()

if __name__ == "__main__":
    app.run('0.0.0.0')
