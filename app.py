from flask import Flask,render_template,redirect,request,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,TextAreaField,SubmitField
from wtforms.validators import InputRequired
import os
from datetime import date,datetime
from flask_migrate import Migrate
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobsapplication.db"
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
class jobs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    posteddate=db.Column(db.Date,nullable=False)
    employeid=db.Column(db.Integer,nullable=False)
    location=db.Column(db.String(100),nullable=False)
    Description=db.Column(db.String(100),nullable=False)
    salary=db.Column(db.Float,nullable=False)
    cpompany=db.Column(db.String(100),nullable=False)
class jobseeker(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    dateofbirth=db.Column(db.Date,nullable=False)
    phonenumber=db.Column(db.String(10),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    qualification=db.Column(db.String(100),nullable=False)
class employer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    dateofbirth=db.Column(db.Date,nullable=False)
    phonenumber=db.Column(db.String(10),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    employerrole=db.Column(db.String(100),nullable=False)
class jobsapplied(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    jobsid=db.Column(db.Integer,nullable=False)
    jobseekerid=db.Column(db.Integer,nullable=False)
    applieddate=db.Column(db.Date,nullable=False)
with app.app_context():
    db.create_all()
#home page
@app.route("/")
def index():
    return render_template("index.html")
#login page
@app.route("/login")
def login():
    user = ""
    buttonclick=True
    return render_template("login.html",buttonclick=buttonclick)
#page checks login is jobseeker or employer
@app.route("/login/<string:user>")
def loginuser(user,message=""):
    buttonclick=False
    return render_template("login.html",user=user,buttonclick=buttonclick,message=message)
#loginsuccess page
@app.route("/loginsuccess/<string:user>",methods=["POST"])
def loginsuccess(user):
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
    if user == "jobseeker":
        userdetails=jobseeker.query.filter_by(username=username).first()
        if userdetails:
            if username == userdetails.username:
                if password == userdetails.password:
                    return render_template("profile.html",userdetails=userdetails,user=user)
                else :
                    message = "incorrect password"
                    return redirect(url_for("loginuser",user=user,message=message))
        else :
            meassage = "incorrect username and password"
            return redirect(url_for("loginuser",user=user,message=message))
    if user == "employer":
        userdetails=employer.query.filter_by(username=username).first()
        if userdetails:
            if username == userdetails.username:
                if password == userdetails.password:
                    return render_template("profile.html",userdetails=userdetails,user=user)
                else :
                    message = "incorrect password"
                    return redirect(url_for("loginuser",user=user,message=message))
        else :
            message = "incorrect username and password"
            return redirect(url_for("loginuser",user=user,message=message))
    return redirect("/login")
#register page
@app.route("/register")
def register():
    return render_template("register.html",buttonclick = True)
#page checks register jobseeker or employer
@app.route("/register/<string:user>")
def registeruser(user,meassage="",userdata=""):
    buttonclick=False
    return render_template("register.html",user=user,buttonclick=buttonclick,message=meassage,userdata=userdata)
#registersuccess page
@app.route("/registersuccess/<string:user>",methods=["POST"])
def registersucess(user):
    if request.method == "POST":
        username = request.form.get("username")
        dateofbirth = request.form.get("dateofbirth")
        dateofbirth = datetime.strptime(dateofbirth,"%Y-%M-%d").date()
        role = request.form.get("role")
        phonenumber = request.form.get("phonenumber")
        email = request.form.get("email")
        password = request.form.get("password")
        if password == request.form.get("confirmpassword"):
            if user == "jobseeker":
                userdata = jobseeker(username=username, dateofbirth=dateofbirth,qualification=role, phonenumber=phonenumber, email=email,password=password)
                userdetails = jobseeker.query.filter_by(username=username).first()
                if userdetails:
                    userdata = "username is already taken"
                    return redirect(url_for("registeruser",user=user,userdata=userdata))
                db.session.add(userdata)
                db.session.commit()
                userdetails = jobseeker.query.filter_by(username=username).first()
                return render_template("profile.html",user=user,userdetails=userdetails)
            elif user == "employer":
                userdata = employer(username=username, dateofbirth=dateofbirth, employerrole=role, phonenumber=phonenumber, email=email, password=password)
                userdetails = employer.query.filter_by(username=username).first()
                if userdetails:
                    userdata = "username is already taken"
                    return redirect(url_for("registeruser",user=user,userdata=userdata))
                db.session.add(userdata)
                db.session.commit()
                userdetails = employer.query.filter_by(username=username).first()
                return render_template("profile.html",user=user,userdetails=userdetails)
            else :
                return rendirect("/register")
        else :
            message = "password and confirmpassword not match"
            return redirect(url_for("registeruser",user=user,message=message))
    return redirect("/register")
#searchjobs page
@app.route("/searchjobs/<string:username>",methods=["POST"])
def searchjobs(username):
    if request.method == "POST":
        location = request.form.get("location")
        category = request.form.get("category")
        company = request.form.get("company")
        category = "%"+category+"%"
        jobsdata = jobs.query.filter_by(jobs.Description.like(category),location=location,cpompany=company).all()
        return render_template("searchjobs.html",jobsdata=jobsdata,username=username)
#search page
@app.route("/search/<string:username>")
def search(username):
    return render_template("searchjobs.html",username=username)
#apply page
@app.route("/apply/<string:username>/<int:jobsid>")
def apply(username,jobsid):
    applyjob = True
    if applyjob:
        userid = jobseeker.query.filter_by(username=username).first()
        applydata = jobsapplied(jobsid=jobsid,jobseekerid=userid.id,applieddate=date.today())
        applieddata = jobsapplied.query.filter_by(username=username,jobsid=jobsid).first()
        if applieddata:
            return redirect(url_for("search",username=username))
        db.session.add(applydata)
        db.session.commit()     
        return redirect(url_for("appliedjobs",username=username,userid=userid.id))
#postjobs page
@app.route("/postjobs/<string:username>",methods=["POST"])
def postjobs(username):
    if request.method == "POST":
        title = request.form.get("title")
        location = request.form.get("location")
        salary = request.form.get("salary")
        description = request.form.get("description")
        company = request.form.get("company")
        employeid = employer.query.filter_by(username=username).first()
        jobsdata = jobs(title=title,location=location,salary=salary,Description=description,cpompany=company,posteddate=date.today(),employeid=employeid.id)
        db.session.add(jobsdata)
        db.session.commit()
        return render_template("postjobs.html",username=username)
#post page
@app.route("/posts/<string:username>")
def posts(username):
    return render_template("postjobs.html",username=username)
#appliedjobs page
@app.route("/appliedjobs/<string:username>/<int:userid>")
def appliedjobs(username,userid):
    jobsid = jobsapplied.query.filter_by(jobseekerid=userid).first()
    jobsdata = jobs.query.filter_by(id=jobsid.id).all()
    return render_template("jobsapplied.html",jobsdata=jobsdata,username=username)
#postedjobs page
@app.route("/postedjobs/<string:username>/<int:userid>")
def postedjobs(username,userid):
    jobsdata = jobs.query.filter_by(employeid=userid).all()
    return render_template("jobsposted.html",jobsdata=jobsdata,username=username)
#deletejobs page
@app.route("/deletejobs/<string:username>/<int:jobid>")
def deletejobs(username,jobid):
    jobsdata = jobs.query.get(jobid)
    userid = employer.query.filter_by(username=username).first()
    db.session.delete(jobsdata)
    db.session.commit()
    return redirect(url_for("postedjobs",username=username,userid=userid.id))
#profile page
@app.route("/profile/<string:username>")
def profile(username):
    return render_template("profile.html",username=username)
#deleteaccount page
@app.route("/deleteaccount/<string:user>/<int:userid>")
def deleteaccount(user,userid):
    if user=="jobseeker":
        userdata = jobseeker.query.get(userid)
        jobsdata = jobsapplied.query.get(userid)
    elif user=="employer":
        userdata=employer.query.get(userid)
        jobsdata = jobs.query.get(userid)
    if jobsdata:
        db.session.delete(jobsdata)
        db.session.commit()
    if userdata:
        db.session.delete(userdata)
        db.session.commit()
    return redirect("/")
#logout page
@app.route("/logout")
def logout():
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)