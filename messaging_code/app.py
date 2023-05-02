from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, HiddenField
from wtforms.validators import InputRequired, Length
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])

    def get_time(self):
        return self.timestamp.strftime("%b %d, %Y %H:%M:%S")

class RegisterForm(FlaskForm):
    name = StringField("name", validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("submit")

class LoginForm(FlaskForm):
    name = SelectField("name")
    submit = SubmitField("submit")

    def update_users(self, users):
        self.name.choices = [(user.id, user.name) for user in users]

class MessageForm(FlaskForm):
    recipient_id = HiddenField("recipient_id")
    body = StringField("body", validators=[InputRequired()])
    submit = SubmitField("reply")


@app.route("/")
def index():
    if current_user.is_authenticated:
        users = User.query.limit(10).all()
        users = list(filter(lambda x: x.id != current_user.id, users))
        return render_template("home.html", users=users)
    else:
        login_form = LoginForm()
        login_form.update_users(User.query.all())
        register_form = RegisterForm()
        return render_template("login.html", login_form=login_form, register_form=register_form)

@app.route("/register", methods=["POST"])
def register():
    register_form = RegisterForm()
    
    if register_form.validate_on_submit():
        name = register_form.name.data
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/login", methods=["POST"])
def login():
    login_form = LoginForm()
    login_form.update_users(User.query.all())
    if login_form.validate_on_submit():
        user = User.query.get(login_form.name.data)
        login_user(user)
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/message-thread/<user_id>")
def message_thread(user_id):
    other_user = User.query.get(user_id)
    sent_messages = Message.query.filter_by(sender=current_user, recipient=other_user).all()
    recieved_messages = Message.query.filter_by(sender=other_user, recipient=current_user).all()
    messages = sent_messages + recieved_messages
    messages = sorted(messages, key=lambda x: x.timestamp)
    print(messages)
    message_form = MessageForm()
    return render_template("message-thread.html", messages=messages, message_form=message_form, user_id=user_id)

@app.route("/new-message", methods=["POST"])
def new_message():
    message_form = MessageForm()
    body = message_form.body.data
    recipient_id = message_form.recipient_id.data
    new_message = Message(body=body, sender=current_user, recipient_id=recipient_id)
    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for("message_thread", user_id=recipient_id))

if __name__ == "__main__":
    app.run(debug=True)
