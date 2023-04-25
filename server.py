from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import User, connect_to_db, db
import crud
from jinja2 import StrictUndefined
from forms import NewUserForm, SearchForm, AddPhoto

app = Flask(__name__)
app.secret_key = "DatingAppForMyCapstone"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/users")
def all_users(is_female):
    search_form = SearchForm()
    
    if search_form.validate_on_submit():
        is_female = search_form.is_female.data == 'True'
        users = crud.get_users_by_sex(is_female)
        if is_female:
            users = [user for user in users if user.is_female]
        else:
            users = [user for user in users if not user.is_female]
    else:
        users = crud.get_all_users()

    return render_template('all_users.html', users = users, search_form = search_form)

@app.route("/users/<user_id>")
def show_user(user_id):
    user = crud.get_user_by_user_id(user_id)
    pictures = crud.get_all_pics()
    return render_template("profile.html", user = user, pictures = pictures )
  
@app.route("/profile")
def profile(user_id):
    logged_in_username = session.get("user.username")
    
    if logged_in_username is None:
        flash("You are not logged in!")
    else:
        profile = crud.get_user_by_user_id(user_id)
        return render_template("profile.html", profile = profile)

@app.route("/login", methods=["POST"])
def new_user():
    new_user_form = NewUserForm()

    if new_user_form.validate_on_submit():
        username = new_user_form.username.data
        password = new_user_form.password.data
        bio = new_user_form.bio.data
        email = new_user_form.email.data
        is_female = new_user_form.is_female.data
        new_user = User(username, password, bio, email, is_female)
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
            flash("User Created!!! Please Log In!!!")
        return redirect("/login")
    else:
        flash("Please Try Again")
        return redirect("/login")
    

@app.route("/login", methods=["POST"])
def process_login():
    username = request.form.get("username") 
    password = request.form.get("password")
    user= crud.get_user_by_username(username) 
    if not user or user.password != password: 
        flash("The email or password you entered is incorrect. Please try again.")
        return redirect("/login")
    else:
        session["username"] = user.username 
        flash(f"Welcome back, {user.username}!")
    return redirect("/")
    
@app.route("/logout")
def logout():
    logged_in_username = session.get("username")
    
    if logged_in_username is None:
        flash("You are not logged in!")
        return redirect("/login")
    else:
        del session["username"] #deletes session token for the user
        flash("logged Out!")
        return redirect("/")
    
