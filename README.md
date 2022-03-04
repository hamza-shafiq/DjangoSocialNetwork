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

Run test-cases through the following command:
```
python3 manage.py test
```

#### Database Models:
```
1. Users
2. Posts
3. Post Likes/Dislike
4. User Location
5. Holiday Information
```

#### 3rd Party Integration:
Suggested API: `app.abstractapi.com/`
```
Following are the services used from Abstract API
1. Geolocation
2. JWT
3. Finding Holidays
```

#### Endpoints
```
1. SignUp: "/api/v1/account/register/"
2. Login: "/api/v1/account/login/"
3. Users: "/api/v1/account/users/"
4. Posts CRUD: "/api/v1/social-app/post/"
5. Post Like/Dislike: "/api/v1/social-app/like-dislike/"
```
