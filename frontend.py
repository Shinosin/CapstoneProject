from flask import render_template

def splash():
    return render_template('splash.html')

def index(message=''):
    return render_template('index.html',
                           message=message)

#student and class
def view_student():
    return

#cca
def confirm_cca(cca_name):
        return render_template(
            "add_cca.html",
            page_type="confirm",
            form_meta={
                "action": "/index",
                "method": "POST"
            },
            form_data={
                "name": cca_name 
            })

def add_cca():
        return render_template(
            "add_cca.html",
            page_type="new",
            form_meta={
                "action": "/add_cca?confirm",
                "method": "POST"
            },
            form_data={
                "name": ""
            })

def view_cca():
    return

#activity
def add_activity():
    return

def confirm_activity(data):
    return

def view_activity():
    return    