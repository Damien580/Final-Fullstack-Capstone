from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import User, connect_to_db, db, Picture, Message, Conversation
import crud
from jinja2 import StrictUndefined
from forms import NewUserForm, SearchForm, AddPhotoForm, LoginForm
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user

app = Flask(__name__)
app.secret_key = "DatingAppForMyCapstone"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def home():
    new_user_form = NewUserForm()
    login_form = LoginForm()
    return render_template("home.html", new_user_form=new_user_form, login_form=login_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    new_user_form = NewUserForm()
    
    if login_form.validate_on_submit():

        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                login_user(user)
                flash("logged in")
                
        flash("Either the password or username is incorrect.")

    return render_template("home.html", login_form=login_form, new_user_form=new_user_form)
        
@app.route("/logout")
def logout():
    logged_in_username = session.get("username")
    
    if logged_in_username is None:
        flash("You are not logged in!")
        return redirect("/")
    else:
        del session["username"] 
        flash("logged Out!")
        return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    add_photo_form = AddPhotoForm()
    profile = current_user
    pictures = crud.get_user_pics(profile.id)

    if request.method == "GET":
        conversations = crud.get_all_convo()
        return render_template("profile.html", profile=profile, pictures=pictures, conversations=conversations, add_photo_form=add_photo_form)
    elif add_photo_form.validate_on_submit():
        pic_url = add_photo_form.url.data
        comment = add_photo_form.comment.data
        user_id = current_user.id 
        new_pic = Picture(pic_url=pic_url, comment=comment, user_id=user_id)
        db.session.add(new_pic)
        db.session.commit()
        flash("Picture added!")
        return redirect(url_for("profile"))
    else:
        flash("Picture not added!")
        return render_template("profile.html", profile=profile, pictures=pictures, add_photo_form=add_photo_form)

@app.route("/new_photo")
def new_photo():
    logged_in_username = session.get("user.username")
    new_photo_form = AddPhotoForm()
    
    if logged_in_username is None:
        return ("You are not logged in!!!")
    else:
        if new_photo_form.validate_on_submit():
            username=logged_in_username
            url = new_photo_form.url.data
            comment = new_photo_form.comment.data
            add_photo = Picture(username, url, comment)
            with app.app_context():
                db.session.add(add_photo)
                db.session.commit()
            return render_template("/profile", url=url, username=username, comment=comment)

@app.route("/users")
def all_users():
    search_form = SearchForm()
    is_female = request.args.get('is_female') == 'True' if request.args.get('is_female') else None
    if search_form.validate_on_submit():
        is_female = search_form.is_female.data == 'True'
        users = crud.get_users_by_sex(is_female)
        if is_female:
            users = [user for user in users if user.is_female]
        else:
            users = [user for user in users if not user.is_female]
    else:
        users = crud.get_all_users()

    return render_template('all_users.html', users = users, is_female = is_female)

@app.route("/users/<user_id>")
def show_user(user_id):
    user = crud.get_user_by_user_id(user_id)
    pictures = crud.get_all_pics()
    return render_template("profile.html", user = user, pictures = pictures )

@app.route("/new_user", methods=["GET", "POST"])
def new_user():
    new_user_form = NewUserForm()

    if new_user_form.validate_on_submit():
        username = new_user_form.username.data
        password = new_user_form.password.data
        user_bio = new_user_form.user_bio.data
        user_email = new_user_form.user_email.data
        is_female = new_user_form.is_female.data
        new_user = User(username, password, user_bio, user_email, is_female)
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
            flash("User Created!!! Please Log In!!!")
        return redirect("/")
    else:
        flash("Please Try Again")
        return redirect("/")

@app.route("/conversation")
def show_convo():
    logged_in_username = session.get("user.username")
        
    if logged_in_username is None:
        flash("You are not logged in!!!")
    else:
        messages = crud.get_messages_by_convo()
        return render_template("convo.html", messages = messages)











if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True, port = 8001, host = "localhost")