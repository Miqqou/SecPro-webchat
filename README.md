# SecPro-webchat
A web application for messaging between users securely. Made for Secure programming course of Tampere University.

# Running
- cd backend
- pip install -r requirements.txt
- cd src
- python manage.py migrate
- python manage.py runserver

# Testing
- python manage.py test
- python manage.py axes_reset  // RESETS ALL the login attempt cooldowns
