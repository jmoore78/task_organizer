from flask import Flask

app = Flask(__name__)

app.secret_key = "there’s a difference between knowing the path and walking the path" # used to prevent Cross Site Request Forgery-allows a CSRF token to be generated and stored in the user's session data
