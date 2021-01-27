from flask import Flask, render_template, request, redirect, flash 
from flask_sqlalchemy import SQLAlchemy
import hashlib
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from datetime import datetime

#app configoration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#login_manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# user 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(32), nullable = False)

# category
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    user = db.Column(db.String(20), nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

#post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    heading = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = False)
    user = db.Column(db.String, nullable = True)

#login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#home page
@app.route("/")
def main():
    logout_user()
    return render_template("home.html", categories = Topic.query.all())

#logged page
@app.route("/logged", methods=['GET', 'POST'])
def logged_page():
	if request.method == 'GET':
		return render_template("logged.html", profile = current_user.username, topics = Topic.query.all())
	else:
		name = request.form['name']
		desc = request.form['desc']
		record = Topic(name = name, description = desc, user = current_user.username)
		db.session.add(record)
		db.session.commit()
		return redirect('/logged')


#signin page
@app.route("/signin", methods=['GET', 'POST'])
def log_page():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['username']
        if len(username) > 20:
            flash("Try agai! Password is must be at most 20 characters!")
            return redirect('/signin')
        password = request.form['password']
        if len(password) < 8:
            flash("Try agai! Password is must be at least 8 characters!")
            return redirect('/signin')
        if len(password) > 32:
            flash("Try agai! Password is must be at most 32 characters!")
            return redirect('/signin')
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = User.query.filter_by(username = username, password = password).first()
        if not user:
            flash("Try agai! Wrong username or password")
            return redirect("/signin")
        else:
            login_user(user)
            return redirect('/logged')
  
#signup page
@app.route("/signup", methods=['GET', 'POST'])
def reg_page():
    if request.method == 'GET':
        return render_template("registration.html")
    else:
        username = request.form['username']
        if len(username) > 20:
            flash("Try agai! Password is must be at most 20 characters!")
            return redirect('/signup')
        user = User.query.filter_by(username = username).first()
        if not user:
            password = request.form['password']
            confirm = request.form['confirm']
            if password != confirm:
                flash("Try agai! Password is not confirmed!")
                return redirect('/signup')
            if len(password) < 8:
                flash("Try agai! Password is must be at least 8 characters!")
                return redirect('/signup')
            if len(password) > 32:
                flash("Try agai! Password is must be at most 32 characters!")
                return redirect('/signup')
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            record = User(username=username, password=password)
            db.session.add(record)
            db.session.commit()
            flash('You were successfully registrate')
            return redirect('/signin')
        else:
            flash('Try agai! This username is already used!')
            return redirect('/signup')
"""
# nov post 
@app.route('/posts/new', methods = ['GET', 'POST'])
def new_post():
	if request.method == 'GET':
		return render_template('newpost.html')
	elif request.method == 'POST':
		header = request.form['name']
		content = request.form['content']
		record = Post(heading = header, content = content, user = "hmm")
		db.session.add(record)
		db.session.commit()
		return redirect('/')
	
# nov komentar
@app.route('/cat/new', methods = ['GET', 'POST'])
def new_cat():
	if request.method == 'GET':
		return render_template('newcat.html')
	elif request.method == 'POST':
		name = request.form["name"]
		category = Category(name = name)
		db.session.add(category)
		db.session.commit()
		return redirect("/")
"""
#main
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)