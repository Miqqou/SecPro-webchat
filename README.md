# SecPro-webchat
A web application for messaging between users securely. Made for Secure programming course of Tampere University.

# Requirements
Python 3.4 (or later)

# Setup
```
cd backend
pip install -r requirements.txt
cd src
python manage.py migrate
python manage.py createsuperuser   # for creating first admin account
```

# Running
```
python manage.py runserver
```

# Testing
```
python manage.py test
python manage.py axes_reset  # RESETS ALL the login attempt cooldowns
```
