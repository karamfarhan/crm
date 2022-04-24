# crm
mini crm for market and mange your  products with your customers 

TO RUN IT :

1 - download the zip file and unpack it

OPEN TERMINAL :

2 - create venv (python -m venv venv_name)
3 - activate you venv :
   windows (venv_name\scripts\activate.bat)
   linux,mac (source venv_name/bin/activate)
   
4 - pip install the requirements file (pip install -r requirements.txt)
5 - run the command to make migrations (python manage.py makemigrations)
6 - run the command to make the tables (python manage.py migrate)
7 - make superuser and give it username and password by running (python manage.py createsuperuser)
9 - run the project by running (python manage.py runserver)
10 - open your browser and go to the link (localhost:8000)
