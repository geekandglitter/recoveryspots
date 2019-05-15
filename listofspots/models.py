# Create your models here
# Note to self: A model in Django is a special kind of object.
# What makes it special is that it is saved in a database
# Think of a model in a database as a spreadsheet, with columns and rows.
# The columns are fields. The rows are data.
from django.db import models


# class is a keyword that says we're defining an object
# the name of my model is Recoverytools
# all object names should start with a capital
# models.Model means that Recoverytools is a model, so Django knows it should be saved in the db
class Recoverytools(models.Model):  # this line defines the model (which is an object)
    #field 1
    rectools = (models.TextField(max_length=9000))
    def __str__(self): # double underscores are called "dunder"
        return self.rectools


class Recoverytoolsbulk(models.Model):  # this line defines the model (which is an object)
    #field 1
    rectoolsbulk = (models.TextField(max_length=9000))
    def __str__(self): # double underscores are called "dunder"
        return self.rectoolsbulk


















# How to Tell Django about changes to our model:
# 1) Type: python manage.py makemigrations listofspots
# 2) Django now prepares a migration file
# 3) Now we have to apply the migration file to our db: python manage.py migrate

# Now to see what Recoverytools looks like:
# 1) To view, add, edit and delete the Recoverytools we've just modeled, we will use Django admin.
# 2) Open the listofspots/admin.py file in the code editor and put in this:
        # from django.contrib import admin
        # from .models import Recoverytools
        # admin.site.register(Recoverytools)
# 3) Now we're ready to look at our model. Remember to run python manage.py runserver first
# 4) Now go to your browser and type the address http://127.0.0.1:8000/admin/. You will see a login page
# 5) Create a superuser, which is a user account that gives me control over everything on the site
# 6) To do so, python manage.py createsuperuser
# 7) When prompted, type your username (lowercase, no spaces), email address, and password. Don't worry  that you can't see the password you're typing in – that's how it's supposed to be. Type it in and press enter to continue. The output should look like this (where the username and email should be your own ones):
    #
    # Username: ola
    # Email address: ola@example.com
    # Password:
    # Password (again):
    # Superuser created successfully.
# 8) Return to your browser. Log in with the superuser's credentials you chose; you should see the Django admin dashboard.


