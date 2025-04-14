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
languages = [translator.translate("telugu",dest="te"),translator.translate("hindi",dest="hi"),translator.translate("english",dest="en")]
languages[0] = [languages[0],"te"]
languages[1] = [languages[1],"hi"]
languages[2] = [languages[2],"en"]
print(languages)
welcomemessage = "hi welcome to software services"
data = "in software services we are providing software installations like coding software or normal software, we can do it in offline or remote, web development front end and back end, this is about software services"
services = ["software installations", "web development (front end back end)"]
ln = "languages"
defaultlanguage = "en"
@app.route("/")
def index():
  return render_template("index.html",languages=languages,welcomemessage=welcomemessage,data=data,services=services,name=name,email=email,phonenumber=phonenumber,ln=ln,defaultlanguage=defaultlanguage)
@app.route("/<string:languageselected>")
def languageselected():
  welcomemessage = translator.translate(welcomemessage,dest=languageselected)
  data = translator.translate(data,dest=languageselected)
  ln = translator.translate(ln,dest=languageselected)
  defaultlanguage = languageselected
  return render_template("index.html",languages=languages,welcomemessage=welcomemessage,data=data,services=services,name=name,email=email,phonenumber=phonenumber,ln=ln,defaultlanguage=defaultlanguage)
if __name__ == "__main__":
  app.run(debug=True)
