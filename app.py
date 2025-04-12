from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from googletrans import Translator
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///nareshgopiproject1.db"
db = SQLAlchemy(app)
name = "kurra naresh gopi"
email = "nareshgopiyadavkurra@gmail.com"
phonenumber = "9390186116"
translator = Translator()
languages = [translator.translate("telugu",src=auto,dest=["telugu"]),translator.translate("hindi",src=auto,dest=["hindi"]),translator.translate("english",src=auto,dest=["english"])]
welcomemessage = "hi welcome to software services"
data = "in software services we are providing software installations like coding software or normal software, we can do it in offline or remote, job applications are government appliactions and it applications, msoffice like excel sheet, power point presentations, documentations, web development front end and back end, this is about software services"
services = ["software installations","msoffice(excel sheet, power point presentation, documentation)", "web development (front end back end)", "job applications(government it)"]
app.route("/")
def index():
  return render_template("index.html")
if __name__ == "__main__":
  app.run(debug=True)
