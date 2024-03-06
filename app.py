from flask import Flask, render_template, request, session
import cv2
import numpy as np
from PIL import Image
from passlib.hash import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/travel_companion'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class user_data(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password)

# Move this outside of the class definition
with app.app_context():
    db.create_all()

@app.route("/")
def hello():
    return render_template('landing.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['new-username']
        email = request.form['new-email']
        password = request.form['new-password']

        new_user = user_data(username=username, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            success_message = f"User '{username}' registered successfully!"
            return render_template('/signup-in.html', success_message=success_message)
        except IntegrityError:
            username_taken = f"'{username}' Username/Email Already Taken !!!"
            return render_template('/signup-in.html', username_taken=username_taken)
    return render_template('/signup-in.html')

@app.route("/signup-in.html")
def signupcaller():
    return render_template('signup-in.html')

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['current-username']
        password = request.form['current-password']

        user = user_data.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['loggedin'] = True
            session['username'] = user.username
            session['password'] = user.password
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            frame = np.array(frame)
            cv2.imwrite('static/images/image.jpeg', frame)
            # Release the Capture Object and close the opencv window
            cap.release()
            cv2.destroyAllWindows()
            return render_template("/index.html")
        else:
            failure_message = f"INVALID USERNAME OR PASSWORD!"
            return render_template('/signup-in.html', failure_message=failure_message)
    return render_template('/signup-in.html')

@app.route("/index.html")
def member1(arg1):
    # return render_template('login.html')
    cap = cv2.VideoCapture(arg1)
    ret, frame = cap.read()
    frame = np.array(frame)
    cv2.imwrite('static/images/image.jpeg', frame)
    # Release the Capture Object and close the opencv window
    cap.release()
    cv2.destroyAllWindows()
    return render_template('index.html')

@app.route("/member.html")
def member2():
    return render_template('member.html')

if __name__ == "__main__":
    app.run(debug=True)
