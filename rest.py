from flask import Flask,render_template,request,redirect,url_for,make_response,jsonify,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2,re
from werkzeug.security import (generate_password_hash,check_password_hash) 
from sqlalchemy.orm import validates 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:vaishnav@localhost:5432/flask_register"
db = SQLAlchemy(app)
migrate  = Migrate(app,db)

#           This is simple flask where table is directly created in pgadmin. this methos is without flasksqlacemy
# @app.route('/regis',methods=['POST'])
# def create():
#     # connect = connection()
#     connect = psycopg2.connect(database="flask_register", 
#                             user="postgres", 
#                             password="vaishnav", 
#                             host="localhost", port="5432")
#     cur = connect.cursor()
    
#     username = request.json['username']
#     email = request.json['email']
#     mobile = request.json['mobile']
#     dob = request.json['dob']
#     firstname = request.json['firstname']
#     lastname = request.json['lastname']
#     # data = [(username,email,mobile,dob,firstname,lastname)]
#     # query = 'INSERT INTO public."register "(username,email,mobile,dob,firstname,lastname) VALUES (%s,%s,%s,%s,%s,%s)'
#     cur.execute('INSERT INTO public."register "(username,email,mobile,dob,firstname,lastname) VALUES (%s,%s,%s,%s,%s,%s)',(username,email,mobile,dob,firstname,lastname,))
#     connect.commit()
#     cur.close()
#     connect.close()
#     return make_response(jsonify({'message': 'user created'}), 201)

        #  Api using flasksqlacemy 

class UserModel(db.Model):
    __tabelname__ = 'User'
    id = db.Column(db.Integer,primary_key = True)
    firstname = db.Column(db.String(),nullable = False)
    lastname = db.Column(db.String())
    password = db.Column(db.String(),nullable = False)
    email = db.Column(db.String(),nullable = False)
    dob = db.Column(db.Date,nullable = False)
    mobile = db.Column(db.Numeric,nullable=False)
    def __init__(self,firstname,lastname,password,email,dob,mobile):
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = email
        self.dob = dob
        self.mobile = mobile

    # @validates('mobile')
    # def validate_mobile(self,key,mobile):
    #     if not mobile:
            

    #         raise AssertionError('Please enter mobile number')
    #     elif mobile >= 10:
    #         raise AssertionError("Lenght of mobile must be 10")
    #     return mobile
    
def validate_feilds(firstname,lastname,mobile):
    if mobile == None:
        return make_response(jsonify({"Error message":"enter Mobile "}),500)
    elif int(mobile) >= 10:
        return make_response({"Error message":"Mobile number must be of 10 digit"},500)
    elif isdigit(firstname):
        print("70")
        return make_response({"Error message":"Only alphabet are allwed in firstname"},500)
    elif isdigit(lastname):
        return make_response(jsonify({"Error message":"Only alphabet are allwed in lastname"}),500)
    else:
        return True

@app.route("/register",methods=['POST'])
def create():
    if request.is_json:
        password = request.json['password']
        email = request.json['email']

        mobile = request.json['mobile']
        dob = request.json['dob']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        print(mobile)
        if len(str(mobile)) > 10:
            return make_response({"Error message":"Mobile number must be of 10 digit"},500)
        elif firstname.isdigit():
            print("70")
            return make_response({"Error message":"Only alphabet are allwed in firstname"},500)
        elif lastname.isdigit():
            return make_response(jsonify({"Error message":"Only alphabet are allwed in lastname"}),500)
        elif not re.match("[^@]+@[^@]+\.[^@]+", email):
            return make_response(jsonify({"Error message":"Incorrect email adddress"}),500)
        elif not re.match('\d.*[A-Z]|[A-Z].*\d', password):
            return make_response(jsonify({"Error message":"Password must contain 1 capital letter and 1 number"}),500)
        elif len(password) < 8 or len(password) > 12:
            return make_response(jsonify({"Error message":"Incorrect password length"}),500)
        password_hash = generate_password_hash(password)
        # print("check hass pass",check_password_hash("scrypt:32768:8:1$8CUvYMMmHVEOxvpW$f9be86dcd789b296374ee274c4e3118e33c90644ee07be6b67ccd4bc20ea6a2a0bb535febfe74c7d613bda86711634a5f02c8f61b822a72d9ddc8cb6d206d1da",'Jhon2jeny'))
        if UserModel.query.filter_by(mobile=mobile,email=email).first():
            return make_response(jsonify({"messagw":"user is already registerd"}),400)
            
        new_user = UserModel(firstname,lastname,password_hash,email,dob,mobile) 
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"messagw":"user is created"}),201)
    else:
        return make_response(jsonify({"messagw":"Please response in json format"}),500)
    
@app.route("/show",methods = ['GET'])
def fetch():
    if request.method == 'GET':
        data = UserModel.query.all()
        for i in data: 
            result = [
                {
                    "id":i.id,
                    "firstname":i.firstname,
                    "lastname":i.lastname,
                    "password":i.password,
                    "email":i.email,
                    "dob":i.dob,
                    "mobile":i.mobile
                }
            ]
            # return render_template("home.html",result=result)
        return {"users":result}
@app.route("/modify/<id>",methods = ['PUT','DELETE','GET'])
def change(id):
  
    if request.method == 'GET':
        i = UserModel.query.get_or_404(id)
        # for i in car:
        #     print(i)
        result = [
        {
            "id":i.id,
            "firstname":i.firstname,
            "lastname":i.lastname,
            "password":i.password,
            "email":i.email,
            "dob":i.dob,
            "mobile":i.mobile
        }
    ]
        return jsonify(result)
    if request.method == 'PUT':
        j = UserModel.query.get_or_404(id)
    
        j['firstname'] = request.json['firstname']
        j['lastname'] = request.json['lastname']
        j['email'] = request.json['email']
        j['password'] = request.json['password']
        j['mobile'] = request.json['mobile']
        j['dob'] = request.json['dob']
        update = {
            'id':id,
            "firstname":j['firstname'],
            "lastname":j['lastname'],
            "password":j['password'],
            "email":j['email'],
            "mobile":j['mobile'],
            "dob":j['dob']
        }
        db.session.add(update)
    
        db.session.commit()
        return {"message":f"user is {update} update"}
    if request.method == 'DELETE':
        user = UserModel.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message":f"user is delete"}
@app.route("/login",methods = ['POST'])
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        user = UserModel.query.filter_by(email=email).first()
        if user:
            password_check = check_password_hash(user.password,password)
            if password_check:
                session['email'] = email
                session['firstname'] = user.firstname
                return make_response(jsonify({"message":"logged in."}),200)
            else:
                return make_response(jsonify({"message":"Incorrect credential"}),400)
        else:
            return make_response(jsonify({"message":"Incorrect credential"}),400)
@app.route("/logout",methods = ['GET'])
def logout():
    if 'email' in session:
        session.pop('email')
    return make_response(jsonify({"message":"log out"}),200)

if __name__ == '__main__':
    app.run(debug==True)