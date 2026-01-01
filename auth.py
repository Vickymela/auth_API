from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"
db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change in real apps
jwt = JWTManager(app)

class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(300),nullable=False)
    password = db.Column(db.String(10))

    def to_dict(self):
        return{
            "name":self.name,
            "email":self.email,
            "password":self.password
        }
@app.route('/')
def home():
    return jsonify({"message":"welcome to my registration"})

@app.route('/register',methods=["POST"])
def register():
    user_data = request.get_json()
    hashed_password = generate_password_hash(user_data["password"])
    info = User(name=user_data['name'],email = user_data['email'],password= hashed_password)
    db.session.add(info)
    db.session.commit()
    return jsonify({"message":"registration successful"})

@app.route('/login',methods=["POST"])
def login():
    user_data = request.get_json()

    email = user_data.get('email')
    password = user_data.get('password')
    user = User.query.filter_by(email=email).first()
    if  not user:
        return jsonify({"error": "invalid email"}),400
    if  check_password_hash(user.password,password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token,)
    else:
        return jsonify({"error":"invalid login"}),400
    

@app.route("/content")
@jwt_required()
def content():
    return jsonify({"message":"this returns the main content of the app"})





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
