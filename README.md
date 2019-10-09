# python-bangazon-api-template

After cloning project, open up your terminal, cd into the project. Then execute these commands:
python -m venv bangazonAPIEnv
source ./bangazonAPIEnv/bin/activate
If this command doesnt work, cd into the environent, cd into the scripts directory, and run activate.bat
pip install -r requirements.txt

This set of commands sets up the database
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata user
python manage.py loaddata customer
python manage.py loaddata categorytype
python manage.py loaddata payment
python manage.py loaddata product
python manage.py runserver  

This should get the API up and working. 