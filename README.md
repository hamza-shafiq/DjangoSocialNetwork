## Django Social Network Application

Basic Python Django Application with DRF & JWT Authentication.

### Setup:
Clone the git repo from the command below:
```
git clone git@github.com:hamza-shafiq/DjangoSocialNetwork.git
```

Go to the project root directory:
```
cd social_app
```

Create virtual environment & install dependencies:
```
python3 -m venv venv
pip3 install -r requirements.txt
```

Currently we are using `sqlite` database just for quick setup.
Following are the commands to create & apply migrations to database
```
python3 manage.py makemigrations
python3 manage.py migrate
```

Run django server through the following command:
```
python3 manage.py runserver
```

#### Database Models:
```
1. Users
2. Posts
3. Post Likes/Dislike
4. User GeoLocation
```

#### 3rd Party Integrations:
```
1. Geolocation
2. JWT
3. Finding Holidays
```