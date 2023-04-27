from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import User, connect_to_db, db, Picture, Message, Conversation
import crud
from jinja2 import StrictUndefined
from forms import NewUserForm, SearchForm, AddPhotoForm
from flask_login import LoginManager, login_user, UserMixin, login_required, current_user

app = Flask(__name__)
app.secret_key = "DatingAppForMyCapstone"
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def home():
    new_user_form = NewUserForm()
    return render_template("home.html", new_user_form=new_user_form)

@app.route("/login", methods=['GET', 'POST'])
def process_login():
    username = request.form.get("username") 
    password = request.form.get("password")
    user= crud.get_user_by_username(username) 
    
    if user and user.password == password:
        pictures = crud.get_user_pics(user.id)   
        session["username"] = user.username 
        flash(f"Welcome back, {user.username}!")
        add_photo_form = AddPhotoForm()
        return render_template("/profile.html",pictures=pictures, profile=user, add_photo_form=add_photo_form)
    
    else:
        flash("The email or password you entered is incorrect. Please try again.")
        return redirect("/")
    
    
        
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
# @login_required
def profile():
    logged_in_username = session.get("user.username")
    add_photo_form = AddPhotoForm()
    profile = None
    pictures = None

    if logged_in_username is None:
        flash("You are not logged in!")
        return redirect(url_for("home"))
    else:
        if request.method == "GET":
            profile = crud.get_user_by_username(logged_in_username)
            pictures = crud.get_user_pics(profile.id)
            conversations = crud.get_all_convo()
            return render_template("profile.html", profile=profile, pictures=pictures, conversations=conversations)
        else:
            if add_photo_form.validate_on_submit():
                pic_url = add_photo_form.url.data
                comment = add_photo_form.comment.data
                user_id = current_user.id 
                new_pic = Picture(pic_url=pic_url,pictures=pictures, comment=comment, user_id=user_id)  
                with app.app_context():
                    db.session.add(new_pic)
                    db.session.commit()
                return render_template("profile.html", pic_url=pic_url, comment=comment, pictures=pictures)
            else:
                flash("Picture not added!")
                return render_template("profile.html", profile=profile, pictures=pictures, add_photo_form=add_photo_form)
    return redirect("/home")
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