from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Task:
    db_name = "todos_list"
    def __init__(self, data):
        self.id = data['id']
        self.task_name = data['task_name']
        self.task_description = data['task_description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
#--------class methods to interface with the database--------
    @classmethod
    def save(cls, data): # bind variable and prepared statements to protect against SQL injection
        query = "INSERT INTO tasks ( task_name , task_description ) VALUES ( %(task_name)s , %(task_description)s );"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(f"save RESULTS: {results}") # INSERT queries will return the ID NUMBER of the row inserted
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tasks;"
        results = connectToMySQL(cls.db_name).query_db(query) # list of dictionaries
        # print(f"get_all Results: {results}")
        return results # used on the show_list page to display all of the current tasks 

    @classmethod
    def get_task_by_id(cls,data): # gets the task id (SELECT query) of the task that needs to be updated, then sends to the controller to be displayed on the edit_task.html page
        query = "SELECT * FROM tasks WHERE id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data) # list of dictionaries stored in the result variable tasks[dict]
        print(f"get_task_by_id Results: {result[0]}")
        return result[0] # returning the dictionary of data using list indexing to the edit_task route function (GET request) 

    @classmethod
    def update(cls,data):
        query = "UPDATE tasks SET task_name=%(task_name)s, task_description=%(task_description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM tasks WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

#--------need a class method that adds deleted task to a deleted_tasks table--------

# --------static method for form validation and flash messages--------
    @staticmethod # will check each new instantiation of the class 
    def validate_new_task(new_task): # new_task parameter is the request.form data recieved from create_task route function (POST request). 
        is_valid = True
        if len(new_task["task_name"]) < 1:
            is_valid = False
            flash("Task Name cannot be blank", "validate_new_task")
        if len(new_task["task_description"]) < 1:
            is_valid = False
            flash("Please describe the task", "validate_new_task")
        query = "SELECT * FROM tasks WHERE task_name = %(task_name)s;" # saving the conditional query to the variable "query"
        results = connectToMySQL(Task.db_name).query_db(query,new_task) # passing the query and the form data to the connectToMySQL function which instatiates the class MySQLConnection (GET request)
        print(results)
        for result in results: # for dictionary in the list of dictionaries in the database table "tasks"
            if len(result["task_name"]) > 0: # checks for a task name that matches when the user enters on the form (looks for duplicates)
                is_valid = False
                flash("That task name already exists", "validate_new_task")
        return is_valid

    @staticmethod
    def validate_edit_task(edit_task):
        is_valid = True
        query = "SELECT * FROM tasks WHERE id = %(id)s;" # saving the conditional query to the variable "query"
        results = connectToMySQL(Task.db_name).query_db(query,edit_task) # passing the query and the form data to the connectToMySQL function which instatiates the class MySQLConnection (GET request)
        for result in results:
            if edit_task["task_name"] != result["task_name"]:
                is_valid = False
                flash("Task Name can't be changed", "validate_edit_task")
            if edit_task["task_description"] == result["task_description"]:
                is_valid = False
                flash("Task Description must be unique", "validate_edit_task")
        return is_valid