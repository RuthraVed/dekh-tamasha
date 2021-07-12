# Welcome To Dekh Tamasha - Watch Movies Worth Your Time

###### tags: `Flask` `RESTful` `SQLAlchemy` `Connexion` `Swagger`

A RESTful API for movies, something similar to IMDB but with potential to be much more.:wink:

For now, there will be 2 levels of access:
-    admin - who can add, remove or edit movies.
-    users - who can just view the movies.

## :file_cabinet: ER Diagram
![](https://i.imgur.com/ABgpmvt.png)


## :gear: Features Implemented
- [X] Create, Read, Update Delete
        - Endpoints for viewing, adding, editting and deleting movies
        
- [X] Search functionality
        -  By movieName or by movieName

- [X] Additional special functionality
        -  Top Movies By popularity or imdb

## :wrench: Features To Be Implemented

- [x] Securing the endpoints using JWT
        - This steps ensures the 2 levels of access

- [x] Deploy on Heroku

## Steps To Use The API

### Requirements

The project requires [Python 3.5](https://www.python.org/downloads/release/python-396/) or higher and
the [PIP](https://pip.pypa.io/en/stable/) package manager.


### Installing and using a virtual environment

#### :computer: Ubuntu setup
1. To install virtualenvwrapper
```shell=1
sudo pip3 install virtualenvwrapper
```
2. Then add the following lines to the end of your **shell startup file** (this is a hidden file name **.bashrc** in your home directory).
```bash=1
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Then reload the startup file by running the following command in the terminal:
```shell=1
source ~/.bashrc
```
Now you can create a new virtual environment with the `mkvirtualenv` command.

After you've created a virtual environment, and called ```workon``` to enter it.
```shell=1
workon name_of_environment
```


### Install the project dependencies

Once in a virtual environment, then use pip3 to install the dependencies

`Flask-SQLAlchemy` `flask-marshmallow` `marshmallow-sqlalchemy` `marshmallow` `connexion[swagger-ui]`

Here's a one line command:
```console=1
$ pip3 install Flask-SQLAlchemy flask-marshmallow marshmallow-sqlalchemy marshmallow connexion[swagger-ui]
```

Or install dependencies from the project's requirements.txt as:
```console=1
$ pip3 install -r requirements.txt
```

:::info
**Note:** Put requirements.txt in the directory where the command will be executed. If it is in another directory, specify the path.
:::

### :pushpin: Initialize The Database
This application currently uses SQLiteDB. If needed other databases like MySql or SQLlite or MongoDB may also be used
```console=1
$ python3 src/db_initializer.py
```

### :no_entry: Perform Tests
###### status: `inactive`
Run all tests
```console=1
$ python3 -m pytest
```

### Finally Run Application

Run the application which will be listening on port `5000`.

```console
$ python3 src/app.py
```

## API Endpoints

After the app is running, one can access the `Swagger2.0` API documentation at:

```
http://localhost:5000/api/ui
```

-- Abhishek Dev
