#### Hello everyone, this is my first project where I implemented the backend part with the `Django framework`. I hope you enjoy it.


#### This project is written with `Django version 6`. To find out what version of Python this version of Django works with, you can refer to the [django](https://docs.djangoproject.com/en/6.0/releases/6.0/#python-compatibility)

#### Of course, I have also uploaded this project with `Docker`, which uses Python version `3.12.13`, which we will discuss later.

# Run with Docker

> *Linux*

##### To run on Linux, make sure you have `Docker` and `Docker compose` installed on your system. If you don't have it installed, visit [Docker](https://docs.docker.com/desktop/setup/install/linux/) and install it according to your Linux distribution.

## 1. clone project

First go to your desired folder and then open the terminal. Make sure the terminal path shows your desired folder then enter the following command in the terminal:

```
git clone https://github.com/GHESHAE7/shop.git
```

When you run the following command, a folder called shop will be created that contains the project files and everything you need.


## 2. Creating the .env file

In the same shop folder, create a new file called `.env`.

In Docker we are working with `postgresql` database version 17. For this reason I put the database information in the `.env` file and when the project is run it will take its information from this file.

Copy this information into the `.env` file for database settings:

```
# postgres
ENGINE=django.db.backends.postgresql
NAME=name database
USER=username
PASSWORD=password user
HOST=postgres
PORT=5432
```

Of course, you can choose the database name, username, and password yourself, but you must also change the environment values ​​in the `docker-compose.yml` file. Match these values ​​in the `.env` file with the environments.

```
POSTGRES_PASSWORD: PASSWORD
POSTGRES_USER: USER
POSTGRES_DB: NAME
```

The `SECRET_KEY` variable in Django is read from the `.env` file. Of course, you can set its value to anything, but to ensure that it is not guessable, add this section to the `.env` file as well.

```
# secret key
SECRET_KEY=anything
```

This project uses email to activate accounts, forget passwords, etc. Add the following to the `.env` file:

```
# email
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=app password
```

Fill in the `EMAIL_HOST` and `EMAIL_HOST_PASSWORD` values ​​based on your information.

## 3. Project implementation


To run the project, simply run the following command in your terminal in the shop folder:

```
sudo docker compose up --build
```

Your project has been successfully implemented and you can enter the `http://127.0.0.1:8000` in your browser to view it.

To stop the project, enter the following command:

```
sudo docker compose down
```

# Run manually

Follow the steps below to install.

## 1. Clone Project

> *Linux*

In Linux, first open the `Terminal` application and navigate to the folder you want for example:
```
cd Dowloads/
```

Then clone the project:
```
git clone https://github.com/GHESHAE7/shop.git
```
And go to the project folder with the following command:
```
cd shop/
```
You are on this path now. `username@host:~/Downloads/shop`

> *Windows*
>
In Windows, first open the `Git Bash` application and navigate to the folder you want for example:

```
cd Documents/
```

Then clone the project:
```
git clone https://github.com/GHESHAE7/shop.git
```
And go to the project folder with the following command:
```
cd shop/
```
You are on this path now. `username@host MINGW64 ~/Documents/shop`

## 2. create virtual environment

> *Linux*
>

The first step is to create a virtual environment:
```
python3 -m venv .venv
```
The second step is to activate the virtual environment:
```
source .venv/bin/activate
```
After activating the virtual environment, you will see this section in your terminal address `((venv) ) username@host:~/Downloads/shop`

> *Windows*
>

The first step is to create a virtual environment:
```
python -m venv .venv
```
The second step is to activate the virtual environment:
```
source .venv/Scripts/activate
```
After activating the virtual environment, you will see this section in your terminal address `(.venv) username@host MINGW64 ~/Documents/shop`

## 3. Install requirements
> *Linux & Windows*
> 
Now it's time to install the packages in the `requirements.txt` file:

```
pip install -r requirements.txt
```

## 4. Config database

In the `main` branch of the project, it works with a `postgresql` database. First create a new database in `postgresql`. Then create a file called `.env` in your project folder `~/Downloads/shop` and fill these values ​​according to your database specifications.

```
# postgres
ENGINE=django.db.backends.postgresql
NAME=name database
USER=username
PASSWORD=password
HOST=ip or domain
PORT=port
```

To use `sqlite3` database, you need to change the `DATABASE` values ​​in the vongi file and replace it with the following value:

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Click to install [sqlite3](https://sqlite.org/).

`Note: If the db.sqlite3 file does not exist in the project folder, create it.`

## 7. Config Email & Secret key

This project has placed the required information in the `.env` file to send emails, as well as the `secret_key` in the project `/config/settings.py`. Place the following texts in the `.evn` file.

```
# email
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=app passwprd

# secret key
SECRET_KEY=secret key
```

## 6. Migrations
Then type this command in your terminal to prepare the database.

```
python manage.py migrate
```

## 6.Start the project

Now everything is fine. You can run the project with the following command

```
python manage.py runserver
```




