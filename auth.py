from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"
db = SQLAlchemy(app)

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
    info = User(name=user_data['name'],email = user_data['email'],password= user_data['password'])
    db.session.add(info)
    db.session.commit()
    return jsonify({"message":"registration successful"})

@app.route('/login',methods=["POST"])
def login():
    user_data = request.get_json()

    email = user_data.get('email')
    password = user_data.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "login sucessful",
                        "name":user_data["name"],
                        "email":user_data["email"]
        })
    else:
        return jsonify({"error":"this user does not exist"})








if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
