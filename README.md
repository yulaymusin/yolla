# Yolla
A web forum with some unique features built with the Django Python web framework.

## Running Yolla locally with sample data
### Project cloning
```commandline
git clone https://github.com/yulaymusin/yolla.git
virtualenv -p python3 venv_yolla
source venv_yolla/bin/activate
cd yolla/
pip install -r requirements.txt
echo -e "SECRET_KEY = 'django-insecure-your-secret-key'\n\nDATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.postgresql_psycopg2',\n        'NAME': 'yolla',\n        'USER': 'yollauser',\n        'PASSWORD': 'pwd',\n        'HOST': 'localhost',\n        'PORT': '5432',\n    }\n}\n\nSERVER_EMAIL = ''\nDEFAULT_FROM_EMAIL = ''\nADMINS = [('yolla', 'mail@mail.yolla'), ]\nMANAGERS = [('yolla', 'mail@mail.yolla'), ]\n\nEMAIL_HOST = 'smtp-mail.yolla.yolla'\nEMAIL_HOST_USER = 'mail@mail.yolla'\nEMAIL_HOST_PASSWORD = 'pwd'\nEMAIL_USE_TLS = True\nEMAIL_PORT = 587\n\nPROTOCOL = 'https'\nDOMAIN = 'yolla.yolla'\nSITE_NAME = 'Yolla'\n" > yolla/settings_production.py```
```
### Installing PostgreSQL using Docker
```commandline
sudo docker run --name postgres -p 54321:5432 -e POSTGRES_PASSWORD=123 -d postgres:14.5
sudo apt-get install -y postgresql-client
```
### Get sample data (static and media)
```commandline
wget https://github.com/yulaymusin/yolla_sample_data/archive/refs/heads/master.zip
unzip master.zip
mv yolla_sample_data-master/media/ .
mv yolla_sample_data-master/static/img/ static/
mv yolla_sample_data-master/docs/ .
rm -rf yolla_sample_data-master/ master.zip
```
### Create database
```commandline
psql -U postgres -h 127.0.0.1 -p 54321
```
enter 123 and then
```commandline
CREATE DATABASE yolla;
\q
```
### Import sample data to database
```commandline
psql yolla < docs/yolla_sample_data.pg_dump postgres -h 127.0.0.1 -p 54321
```
enter 123
### Runserver with DEBUG = True
```commandline
sed -i 's/DEBUG = False/DEBUG = True/' yolla/settings.py
python manage.py runserver
```
### Open Yolla in Web-browser
[127.0.0.1:8000](http://127.0.0.1:8000/)

#### Log in with users:
* <b>admin</b> (is_superuser = True, is_staff = True)
* <b>staff</b> (is_superuser = False, is_staff = True)
* <b>user1</b> (is_superuser = False, is_staff = False)
* <b>user2</b> (is_superuser = False, is_staff = False)
* <b>user3</b> (is_superuser = False, is_staff = False)

#### Passwords for all users are the same:
* <b>password123</b>