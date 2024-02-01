# SecPro-webchat
A web application for messaging between users securely. Made for Secure programming course of Tampere University.

# Documentation
[Documentation](Documentation.pdf)
covers the program by providing detailed description, more insight into its structure, and solutions for secure programming. It also explains the security testing procedures used. Furthermore, the documentation includes a comprehensive list acknowledgments on what must, should and could be improved.


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
