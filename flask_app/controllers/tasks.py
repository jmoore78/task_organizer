from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.task import Task
# Route Security: Although a small application, I chose to keep the GET and POST routes separate 
# as a good practice to reduce the chance of template injection. Routes in Flask are mapped to the Python route function.


@app.route('/') # home page route that displays the task entry form (view function)
def home():
    return render_template("index.html") # home page html

@app.route('/create/task', methods=['POST']) # not visible to the user-this route collects info from the form for data handling
def create_task():
    if not Task.validate_new_task(request.form): # form validation for the new task entry. if it fails, redirected to the form with an error message
        return redirect('/')
    data = {
        "task_name": request.form['task_name'],
        "task_description": request.form['task_description']
    }
    Task.save(data)
    return redirect('/') # redirects back to home for the user to retry the task entry

@app.route('/edit/task/<int:id>') # route variable allows for the id to be passed to the edit_task page and used in the query (class method get_task_by_id)
def edit_task(id):
    data = {
        "id": id
    }
    return render_template("edit_task.html", edit=Task.get_task_by_id(data)) # calls the class method which processes the query which is returned and stored in the edit variable. Jinja is used to display the edit variable data (dictionary) using dot notation 

@app.route('/update/task', methods=['POST'])
def update_task(): # after the edit_task GETs the task id (and other packaged data) from the database in the edit_task route function
    if not Task.validate_edit_task(request.form):
        return redirect('/show/list') 
    data = {
        "task_name": request.form['task_name'],
        "task_description": request.form['task_description'],
        "id": request.form['id']
    }
    Task.update(data)
    return redirect('/show/list')

@app.route('/show/list') # task list route where the tasks are displayed for the user to see
def show_list():
    return render_template("show_list.html", tasks=Task.get_all()) # 

@app.route('/destroy/task/<int:id>')
def destroy_task(id):
    data = {
        "id": id
    }
    Task.destroy(data)
    return redirect('/show/list')