from subprocess import Popen
import webbrowser  
import os

script_path = os.path.abspath(__file__)

os.chdir(os.path.dirname(script_path))

Popen('python manage.py runserver', shell=True)

webbrowser.open('http://127.0.0.1:8000/chores/user_management/login/')
