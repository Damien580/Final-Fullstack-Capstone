from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from forms import NewUserForm, SearchForm, AddPhotoForm, LoginForm, MessageForm
from model import User, connect_to_db, db, Picture, Message
import crud

UPLOAD_FOLDER = '/Users/damienredd/School/DevMountain/Python F35/Capstone/static/pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = "DatingAppForMyCapstone"
app.config['UPLOADED_PHOTOS_DEST'] = 'static/pics'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

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

@app.route("/new_user", methods=["GET", "POST"])
def new_user():
    new_user_form = NewUserForm()

    if new_user_form.validate_on_submit():
        new_username = new_user_form.new_username.data
        new_password = new_user_form.new_password.data
        user_bio = new_user_form.user_bio.data
        user_email = new_user_form.user_email.data
        is_female = new_user_form.is_female.data
        is_female = is_female == 'true'
        new_user = User(new_username, new_password, user_bio, user_email, is_female)
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
            flash("User Created!!! Please Log In!!!")
        return redirect("/")
    else:
        flash("Please Try Again")
        return redirect("/")
    
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
                flash("Logged In!")
            else:    
                flash("Either the password or username is incorrect!")

    return render_template("home.html", login_form=login_form, new_user_form=new_user_form)
        
@app.route("/logout")
def logout():
    logout_user()
    flash("You are Logged Out!")
    return redirect("/")

    
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    add_photo_form = AddPhotoForm()
    profile = current_user
    pictures = crud.get_user_pics(profile.id)

    if add_photo_form.validate_on_submit():
        pic_url = add_photo_form.url.data
        comment = add_photo_form.comment.data
        user_id = current_user.id 
        new_pic = Picture(pic_url=pic_url, comment=comment, user_id=user_id)
        db.session.add(new_pic)
        db.session.commit()
        add_photo_form.process() 
        
        if new_pic:
            flash("Picture added!")
            return redirect(url_for("profile"))
        else:
            flash("Picture not added!!!")
    return render_template("profile.html", profile=profile, pictures=pictures, add_photo_form=add_photo_form)

@app.route("/users")
@login_required
def all_users():
    search_form = SearchForm()
    is_female = request.args.get('is_female')
    if is_female:
        is_female = is_female == 'True'
        users = crud.get_users_by_sex(is_female)
    else:
        users = crud.get_all_users()
    
    return render_template('all_users.html', users=users, is_female=is_female, search_form=search_form)

@app.route("/users/<int:id>")
@login_required
def show_user(id):
    user = crud.get_user_by_user_id(id)
    pictures = crud.get_user_pics(id)
    return render_template("user.html", user=user, pictures=pictures)

@app.route('/delete_picture/<int:pic_id>', methods=['POST'])
@login_required
def delete_picture(pic_id):
    pic = Picture.query.get(pic_id)
    if pic and pic.user_id == current_user.id:
        db.session.delete(pic)
        db.session.commit()
        flash('Picture deleted!')
    else:
        flash('Picture not found or unauthorized to delete.')
    return redirect(url_for('profile'))

@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    messages = []
    senders = User.query.all()
    message_form = MessageForm()
    message_form.recipient.choices = [(user.id, user.username) for user in User.query.all()]
    
   
    sender_id = request.args.get('sender')
    if sender_id is not None:
        messages = crud.get_all_messages(sender_id=int(sender_id))
    else:
        messages = crud.get_all_messages()
    
    if message_form.validate_on_submit():
        sender_id = current_user.id
        recipient_id = int(message_form.recipient.data)
        message = message_form.message.data  
        new_message = Message(sender_id=sender_id, recipient_id=recipient_id, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent!')
    
    sender_id = request.args.get('sender')
    
    if sender_id:
        messages = crud.get_all_messages(sender_id=int(sender_id), recipient_id=current_user.id)
    else:
        messages = []
   
    
    return render_template('messages.html', message_form=message_form, messages=messages, senders=senders)

    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True, port = 8001, host = "localhost")