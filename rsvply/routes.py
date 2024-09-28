from rsvply import app, bcrypt, db, IST
from flask import url_for, render_template, redirect, flash, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required

from rsvply.models import User, Event, RSVP
from rsvply.forms import LoginForm, RegistrationForm, EventForm,RSVPForm

from datetime import datetime
import hashlib, uuid, pytz, base64
import qrcode as qr
from io import BytesIO


def generate_qr(hash):
    img = qr.make(hash)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Encode image as base64
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    # Pass the base64 encoded image to the template
    return img_base64

def check_for_duplicates(email,event_id):
    entry = RSVP.query.filter_by(email=email, event_id=event_id).first()
    return False if entry else True


@app.route("/")
def index():
    return render_template("index.html")



# Login and Register----------------------------
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
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
    events = Event.query.order_by(Event.id.desc()).filter_by(user_id=current_user.id)
    print(current_user.id)
    return render_template("home.html", events=events)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))



def generate_hash(field1, field2):
     unique_string = f"{field1}{field2}{uuid.uuid4()}"

     return hashlib.sha256(unique_string.encode()).hexdigest()

# Event ------------------------------------
@app.route("/create-event", methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    
    if form.validate_on_submit():
        hash = generate_hash(form.title.data, current_user.id)
        hash = hash[:12]

        # localize date and expiry        
        date_time_ist= form.date.data.astimezone(IST)
        expiry_ist= form.expiry.data.astimezone(IST)


        event = Event(title=form.title.data, datetime=date_time_ist,expiry=expiry_ist,
                       description = form.description.data, location=form.location.data, user_id = current_user.id,
                       hash=hash,author=current_user)
        db.session.add(event)
        db.session.commit()


        flash('Submitted', 'success')
        return redirect(url_for('home'))


    now=datetime.now(IST).strftime('%Y-%m-%dT%H:%M')
    return render_template("event/event.html", form=form, min_date=now)

@app.route("/event/<string:event_hash>", methods=['GET', 'POST'])
def event(event_hash):
    event = Event.query.filter_by(hash=event_hash).first_or_404()
    rsvps = RSVP.query.filter_by(event_id=event.id)
    return render_template('event/event-page.html', title=event.title, event=event, rsvps=rsvps)




# RSVP -------------------------------------------------------------
@app.route("/rsvp/<string:event_hash>", methods=['GET', 'POST'])
def rsvp(event_hash):
    print("RSVP FUNCTION CALLED")
    event = Event.query.filter_by(hash=event_hash).first()
    form = RSVPForm()
    qr = None

    if datetime.now(IST) > event.expiry.astimezone(IST) : 
        flash('Link has expired','info')
        return redirect(url_for('home'))


    if form.validate_on_submit():
        if check_for_duplicates(form.email.data, event.id):
            print('SUBMITTED')
            rsvp_hash = generate_hash(form.username.data, form.email.data)
            rsvp = RSVP(name=form.username.data, email=form.email.data, attending=form.attending.data, event_id=event.id, hash=rsvp_hash)
            db.session.add(rsvp)
            db.session.commit()
            qr = generate_qr(rsvp_hash)
        else :
            flash('That email has already been registered', 'danger')
            # print('EMAIL EXISTS')
            # rsvp_hash = RSVP.query.filter_by(email=form.email.data, event_id=event.id).first().hash
            # qr = generate_qr(rsvp_hash)

    

    return render_template("rsvp.html", form=form, event=event, qr_code_data=qr)


@app.route('/process_qr', methods=['POST'])
def process_qr():
    # Get the scanned QR code data from the POST request
    data = request.json.get('scanned_data')
    
    #Do something with the data (e.g., check it against your database)
    if data:
        attendee = RSVP.query.filter_by(hash=data).first_or_404()
        attendee.checked_in = True
        db.session.commit()
    
    # return render_template("rsvp.html", event=event)