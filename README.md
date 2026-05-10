# petCenter
PetCenter (Django)
Web application for managing animal adoption processes, including user registration, authentication, and email verification.

Features:
User registration and login system
Email verification using token
Secure authentication system
Role-based access (center, client)
Creates/edits pets (main product)
Management of adoption requests

Tech Stack:
Django
SQLite
Python
Basic HTML/CSS/JS

How to run?
git clone https://github.com/Linda0Sousa/PetCenter.git
cd PetCenter; cd petCenter;

python -m venv venv
source venv/bin/activate  #linux
pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic

gunicorn petCenter.wsgi:application

open your broswer and go to:
http://127.0.0.1:8000


Setup:
Create a .env file in the root of the project:
touch .env

Add the required variables:
SECRET_KEY=your_secret_key
EMAIL_USER=your_email
EMAIL_PASSWORD=your_password