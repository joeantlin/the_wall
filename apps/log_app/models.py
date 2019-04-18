from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors["fname"] = "First Name should be at least 2 characters"
        if len(postData['fname']) < 2:
            errors["lname"] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email is not formatted correctly"
        elif User.objects.filter(email=postData['email']):
            errors["email2"] = "That email has already been taken"
        if not postData['pass'] == postData['pwc']:
            errors["pwc"] = "Your passwords do not match"
        elif len(postData['pass']) < 8:
            errors["pass"] = "Password should be at least 8 characters"
        return errors

    def log_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid Email"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"User: {self.first_name} {self.last_name} {self.email}"

class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
