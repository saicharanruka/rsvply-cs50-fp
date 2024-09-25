from rsvply import app, bcrypt, db
from flask import url_for, render_template, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required

from rsvply.models import User, Event
from rsvply.forms import LoginForm, RegistrationForm, EventForm, ist_timezone

from datetime import datetime


@app.route("/")
def index():
    return render_template("index.html")



# Login and Register----------------------------
@app.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#------------------------------------------------



@app.route("/home")
@login_required
def home():
    events = Event.query.filter_by(user_id=current_user.id)
    print(current_user.id)
    return render_template("home.html", events=events)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# Event ------------------------------------
@app.route("/create-event", methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    

    if form.validate_on_submit():
        event = Event(title=form.title.data, date=form.date.data,
                       description = form.description.data, location=form.location.data, user_id = current_user.id,
                       author=current_user)
        db.session.add(event)
        db.session.commit()


        flash('Submitted', 'success')
        return redirect(url_for('home'))


    min_date=datetime.now(ist_timezone).strftime("%Y-%m-%d")
    return render_template("event/event.html", form=form, min_date=min_date)