from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = []     # array of error messages
        if len(postData["first_name"]) == 0:
            # if first name has not been entered
            errors.append("Please enter a first name.")
        elif len(postData["first_name"]) < 2:
            errors.append("First name must be between 2-45 characters.")
        elif not re.search(r'^[A-Za-z]+$', postData["first_name"]):
            errors.append("First name must be letters only.")
        if len(postData["last_name"]) == 0:
            errors.append("Please enter a last name.")
        elif len(postData["last_name"]) < 2:
            errors.append("Last name must be between 2-45 characters.")
        elif not re.search(r'^[A-Za-z]+$', postData["last_name"]):
            errors.append("Last name must be letters only.")
        if len(postData["email"]) == 0:
            errors.append("Please enter an email address.")
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', postData["email"]):
            errors.append("Invalid email address.")
        elif len(User.objects.filter(email=postData["email"])) > 0:
            # if list of users w/ this email is empty
            errors.append("Email address is already registered.")
        try:
            dob = datetime.strptime(postData["dob"], "%m/%d/%Y")
        except ValueError:
            errors.append("Invalid date of birth entered. Use M/D/YYYY format.")
        else:
            if datetime.now() < dob:
                errors.append("Future date of birth entered.")
        if len(postData["password"]) < 8:
            errors.append("Password must be 8 or more characters.")
        if postData["confirm"] != postData["password"]:
            errors.append("Passwords do not match.")
        if len(errors) == 0:
            try:
                user = User.objects.create(first_name=postData["first_name"], last_name=postData["last_name"],email=postData["email"],dob=dob,pw_hash=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()))
            except OverflowError:
                # Encountered an error when attempting to input 1/1/1900 as date of birth
                errors.append("Invalid date of birth.")
                return (False, errors)
            return (True, user)
            # returns (success code, user object)
        else:
            return (False, errors)
            # returns (failure, error list)

    def authenticate(self, postData):
        if "email" in postData and "password" in postData:
            try:
                user = User.objects.get(email=postData["email"])
            except User.DoesNotExist:
                return (False, "Invalid email/password combination.")
            pw_match = bcrypt.hashpw(postData['password'].encode(),user.pw_hash.encode())
            if pw_match:
                return (True, user)
            else:
                return (False, "Invalid email/password combination.")
        else:
            return (False, "Please enter login info.")


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    dob = models.DateTimeField()
    pw_hash = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
