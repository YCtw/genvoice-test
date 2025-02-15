import sqlalchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

#Basic setup
app = Flask(__name__)

#Database setup
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///health.db" #This is for local environment testing
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Clinicians(db.Model):
    __tablename__ = "clinicians"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=False)
    user_name = db.Column(db.Text, nullable=False, unique=True)
    pwd = db.Column(db.Text, nullable=False, unique=False)
    roles = db.Column(db.String(6), nullable=False, unique=False)

class Cases(db.Model):
    __tablename__ = "cases"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=False)
    description = db.Column(db.Text, nullable=False, unique=False)

with app.app_context():
    db.create_all()



@app.route("/", methods=["GET", "POST"])
def homepage():
    return "hi"

#Register clinician
@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        name = data.get("name")
        user_name = data.get("user_name")
        pwd = data.get("pwd")

        if not name or not user_name or not pwd:
            return jsonify({"error": "Missing required columns: name, username, password"}), 400

        check_regis = db.session.query(Clinicians).filter(Clinicians.user_name == user_name).first()
        if check_regis:
            return jsonify({"error": "Username has already been taken"}), 409

        #Register for new clinician
        new_clinician = Clinicians(name=name, user_name=user_name, pwd=pwd, roles="Junior")
        db.session.add(new_clinician)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 200


#Login clinician
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        user_name = data.get("user_name")
        pwd = data.get("pwd")

        if not user_name or not pwd:
            return jsonify({"error": "Missing required columns: username, pwd"}), 400

        check_login_username = db.session.query(Clinicians).filter(Clinicians.user_name == user_name).first()
        if not check_login_username:
            return jsonify({"error": "Username not existed, you should register first"}), 404

        check_login_pwd = db.session.query(Clinicians).filter(Clinicians.user_name == user_name, Clinicians.pwd == pwd).first()
        if not check_login_pwd:
            return jsonify({"error": "Wrong password"}), 401
        #Username match password
        return jsonify({"message": f"Login successful, role: {check_login_pwd.roles}"}), 200


#Promote clinician
@app.route("/promote", methods=["POST"])
def promote():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        id = data.get("id")

        check_promote = db.session.query(Clinicians).filter(Clinicians.id == id).first()
        if not check_promote:
            return jsonify({"error": "User id not existed"}), 404

        if check_promote.roles == "Senior":
            return jsonify({"error": "User has already been Senior"}), 409

        #Promote the user
        check_promote.roles = "Senior"
        db.session.commit()
        return jsonify({"message": "User promoted to Senior"}), 200


#Demote clinician
@app.route("/demote", methods=["POST"])
def demote():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        id = data.get("id")

        check_demote = db.session.query(Clinicians).filter(Clinicians.id == id).first()
        if not check_demote:
            return jsonify({"error": "Username id not existed"}), 404

        if check_demote.roles == "Junior":
            return jsonify({"error": "Username has already been Junior"}), 409

        #Demote the user
        check_demote.roles = "Junior"
        db.session.commit()
        return jsonify({"message": "User demoted to Junior"}), 200


#View all cases
@app.route("/cases", methods=["GET"])
def cases():
    if request.method == "GET":
        cases = db.session.query(Cases).all()

        #Convert each SQLAlchemy object to a dictionary
        cases_list = [{"id": user.id, "name": user.name, "description": user.description} for user in cases]
        return jsonify({"cases": cases_list}), 200


#Add case
@app.route("/case", methods=["POST"])
def case():
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        name = data.get("name")
        description = data.get("description")

        if not name or not description:
            return jsonify({"error": "Missing required columns: name, description"}), 400

        #Add new case
        new_case = Cases(name=name, description=description)
        db.session.add(new_case)
        db.session.commit()
        return jsonify({"message": "Case added successfully"}), 200



if __name__ == "__main__":
    app.run(debug=True)