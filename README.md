# shop
This project is my first Django project on GitHub.

## Requirements
This project uses Django version *6*, and to find out what version of Python you need, visit [python_requirement](https://docs.djangoproject.com/en/6.0/faq/install/#what-python-version-can-i-use-with-django) from the Django website.

> linux

## 1.Clone Project

In Linux, navigate to the folder where you want the project to be located.
For example:
```
cd Dowloads/
```

Then clone the project:
```
git clone https://github.com/GHESHAE7/shop.git
```
And go to the project folder with the following command
```
cd shop/
```
You are on this path now. `username@host:~/Downloads/shop`
## 2.create virtual environment
The first step is to create a virtual environment:
```
python3 -m venv .venv
```
The second step is to activate the virtual environment:
```
source .venv/bin/activate
```
After activating the virtual environment, you will see this section in your terminal address `((venv) ) farhan@FARHAN-AZIZI:~/ME/Project/shop`
## 3.Install requirements
Now it's time to install the packages in the requirements.txt file:
```
pip install -r requirements.txt
```
## 4.Config database
In the `main` branch of the project, it works with a `postgresql` database. First create a new database in `postgresql`. Then create a file called `.env` in your project folder `~/Downloads/shop` and fill these values ​​according to your database specifications.
```
ENGINE=django.db.backends.postgresql
NAME=name database
USER=usernam
PASSWORD=password username
HOST=127.0.0.1
PORT=5432
```
In the `sqlite3` branch, there is no need to configure anything, just make sure that `sqlite3` is installed on your system. If `sqlite3` is not installed on your system, go to this [install sqlite3](https://sqlite.org)
## 5.Migrations
Then type this command in your terminal to prepare the database.
```
python manage.py migrate
```
## 6.Start the project
Now everything is fine. You can run the project with the following command
```
python manage.py runserver
```

