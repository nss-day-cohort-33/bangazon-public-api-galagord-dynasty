# Directions to using banagzon-public-api-galagord-dynasty

After cloning project, open up your terminal, cd into the project. Then execute these commands:

```python -m venv bangazonAPIEnv```

```source ./bangazonAPIEnv/bin/activate```

If this command doesnt work, cd into the environent, cd into the scripts directory, and run ```activate.bat```

```pip install -r requirements.txt```

This set of commands sets up the database

```python manage.py makemigrations```

```python manage.py migrate```

```python manage.py loaddata user```

```python manage.py loaddata customer```

```python manage.py loaddata categorytype```

```python manage.py loaddata payment```

```python manage.py loaddata product```

```python manage.py runserver```

This should get the API up and working. 

## To use this app in full, you will need to clone down the "client side" repository as well as this API repository.

[client-side application](https://github.com/nss-day-cohort-33/bangazon-client-application-galagord-dynasty) via HTTP

### Authors

* [Adam Knowels](https://www.linkedin.com/in/adamcoreyknowles/)
* [Shane Miller](https://www.linkedin.com/in/shanethomasmiller/)
* [Melanie Bond](https://www.linkedin.com/in/melanie-jane-007/)
* [Karla Gallegos](https://www.linkedin.com/in/karla-gallegos/)
* [Misty DeRamus](https://www.linkedin.com/in/misty-deramus/)
* [Krystal Gates](https://www.linkedin.com/in/krystalgates/)
