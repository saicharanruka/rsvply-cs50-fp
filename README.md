# RSVP.ly - Efficient Event RSVP and Check-in System

![Screenshot of the RSVP.ly homepage](/homepage.png "RSVP.ly Homepage")

**RSVP.ly** is a simple yet powerful event management system built with **Flask, SQLite, Javascript** and other modern technologies. The application provides a complete solution for managing RSVPs for any event and simplifies attendee check-in with the use of QR codes.

RSVP.ly allows event organizers to send personalized invitations to attendees, generate unique QR codes for each RSVP, and scan these codes to check in attendees seamlessly and track invites at the event.

## Features
1. **QR Code Generation**: Each attendee receives a unique QR code upon RSVP, which acts as their ticket to the event.

2. **QR Code Scanning**: Event organizers can scan the QR code upon arrival for quick and easy check-ins, ensuring a streamlined process without manual attendee lists.

3. Automated RSVP Management: Attendees can confirm their attendance through a web-based form, which automatically updates the event database.

4. Link Expiration: The RSVP link or QR code can be set to expire after a specific date and time, ensuring only timely responses are valid.

5. User-friendly Interface: The app provides a clean and intuitive interface for both event organizers and attendees.

6. Simple Setup: RSVP.ly is easy to deploy and manage, using lightweight technologies like Flask and SQLite, making it ideal for small to mid-sized events.

7. Responsive Design: The app can be accessed across devices, making it convenient for both mobile and desktop users.

## How It Works
- **Event Creation and Invitation** : 
Once the event is created in RSVP.ly, the organizer can invite attendees by sending a personalized RSVP link or form. The link contains essential event details and prompts the attendees to confirm their participation.

- **QR Code Generation**
After the attendee confirms their RSVP, RSVP.ly automatically generates a unique QR code that will serve as the attendee's pass for the event. This QR code is displayed on the web and should be saved to the device for later use.

- **QR Code Scanning and Check-in**
During the event, the organizer can use the built-in QR code scanner to quickly check in attendees. Scanning the QR code confirms the attendee's presence and logs the time of check-in. This process eliminates manual attendee verification and speeds up the check-in process.

- **RSVP Link Expiration**
To ensure that only timely RSVPs are valid, RSVP.ly allows you to set an expiration date for the RSVP form or the QR code. Once the expiration date is reached, the RSVP link or QR code becomes invalid, preventing further responses or entries.

## Technologies Used
**Flask**: A lightweight Python web framework that powers the backend of RSVP.ly. Flask’s simplicity and flexibility make it ideal for small applications like this one.

**SQLAlchemy**: SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

**HTML5 & CSS**: Provides a responsive and user-friendly interface for both attendees and organizers.

**JavaScript (html5-qrcode)**: A JavaScript library used for scanning QR codes using the device's camera, enabling quick check-in without any additional hardware.

Python's qrcode library: Generates unique QR codes for each attendee after they RSVP.


# Installation and Setup
Prerequisites  
- Python 3.x installed on your machine.
- Basic knowledge of Python and Flask.
- Pip for managing Python packages.
- Steps to Set Up RSVP.ly Locally


Clone the Repository:

    git clone https://github.com/saicharanruka/rsvply.git
    cd rsvply
Create a Virtual Environment:

    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install Dependencies: Install all required Python libraries by running:

    pip install -r requirements.txt


Run the Application: Start the Flask development server in Debug mode:

    python app.py  

Access the App: Open your web browser and navigate to:

    http://127.0.0.1:5000/


Directory Structure

    rsvply/
    │
    ├── app.py                # Main Flask application
    ├── templates/            # HTML templates for the app
    ├── static/               # Static files (CSS, JavaScript, images)
    ├── README.md             # Project documentation
    ├── requirements.txt      # List of Python dependencies
    └── __init__.py           # Flask app initialization


# Usage
1. **Create Event**: Use the admin panel or Flask routes to create an event, specifying details like the event name, date, time, and location.

2. **Invite Attendees**: Send RSVP invitations via email or other communication methods. Attendees will fill out a form to confirm their attendance.

4. **Receive QR Codes**: Once attendees RSVP, a unique QR code will be generated for each attendee. This code will be sent via email or displayed on the RSVP confirmation page.

4. **Check-in at Event**: On the event day, use the in-browser QR code scanner (available on both mobile and desktop) to scan attendees’ QR codes for quick check-ins.

5. **Manage RSVPs**: View and manage RSVPs, check-ins, and attendee data via the app's admin interface.

# Extending RSVP.ly
RSVP.ly is designed with simplicity and extensibility in mind. Here are some ways you can extend the application:

1. **Email Notifications**: Add email functionality using Flask-Mail to send QR codes and confirmations via email.
2. **Event Analytics**: Add analytics, such as the number of attendees, peak check-in times, etc.


# Contact Information  
For any inquiries or support, you can contact the project maintainer at:   

Email: saicharanruka@gmail.com  
GitHub: saicharanruka  

---