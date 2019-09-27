# Alpha Web Application
[![build status](https://github.com/Boburbeck/alpha.git)](https://github.com/Boburbeck/alpha.git)

Server side Alpha application.

### Tech


We use:

* [Django] - is a high-level Python Web framework
* [Django REST framework] - Django REST framework is a powerful and flexible toolkit for building Web APIs
* [Postgresql] - open source object-relational database system

And many other libraries.

### Installation

Dillinger requires [Python](https://www.python.org) v3.6+.

Install the dependencies and devDependencies and start the server.
```sh
$ git clone https://github.com/Boburbeck/alpha.git
$ cd alpha
$ pip install virtualenv
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
```
### Postgres
```
$ su postgres
$ psql
postgres=# CREATE DATEBASE alpha;
postgres=# CREATE USER alpha_user WITH ENCRYPTED PASSWORD 'alpha_password';
postgres=# ALTER USER alpha_user WITH SUPERUSER';
```

### Development
```sh
$ python manage.py runserver
```

### Documentation
Api http://localhost:8000/docs/



[Django]: <https://www.djangoproject.com/>
[Django REST framework]: <http://www.django-rest-framework.org/>
[Postgresql]: <https://www.postgresql.org/>
