This is my first interview task. Task 4 Level 2

In this task I created a authentication system with register, login, logout and profile functionality.

To test the project we need to clone the repository or download the repository.
Also u must have python version 3.12 installed in your system. Thereafter you can run the following command sequentially and without encountering any error:
1. pip install pipenv
2. pipenv install
3. pipenv update
4. pipenv check
5. pipenv shell
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py runserver

Afterthat you get an url(http://127.0.0.1:8000/). Going to the link you go to register page.
Here you can register yourself or can go to login page if already registered.
In login page you can log in with your credentials or can go to register page.
after a succesful login you will be redirected to profile page where you can see your name and email and username.
Also you can change your name and email by updating profile.
After that you can logout your profile.
You can not view or go to the profile page until you are logged in.
