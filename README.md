### portfolio

Django app that provide user to registration, storage and  edit  information.

Install notes:  
 0. Python 2.7.6, Django 1.7.10, SQLite
 1. Install **pillow** dependencies: ``sudo apt-get install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev``.  
 2. Clone repository.
 3. In **settings.py** input ``EMAIL_HOST_USER = ''`` and ``EMAIL_HOST_PASSWORD = ''`` which used in registration form.
 4. In **views.py** input ``from_email = ''`` address which used in **register** function. 
 5. In your **env**: ``pip install -r requirements.txt``
