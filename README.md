# jobs portal
this is a web application with python, flask, flask-sqlalchemy

## users
[jobseekers(register, serarch jobs, apply jobs)]
[employers(post jobs, manage jobs)]
[admin(manage users)]

## features
[users(login and register)]
[jobs posting with title, salary, description, location]
[jobs search with filters location, categeory, company]
[users can apply for jobs]
[database to store jobs]

## setup virtualenvironment
python -m venv venv

## activate virtualenvironment
venv\Scripts\activate

## install flask
pip install flask

## install flask-sqlalchemy
pip install flask-sqlalchemy

## folder structure
/.venv
/instance
    jobsapplication.db
/static
    style.css
/templates
    index.html
    jobsapplied.html
    jobsposted.html
    login.html
    postjobs.html
    profile.html
    register.html
    searchjobs.html
app.py
README.md
requirements.txt

## install requirements
pip install -r requirements.txt

## run project
python app.py

## author
kurra naresh gopi