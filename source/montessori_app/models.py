from django.db import models
import re
from datetime import date, datetime 

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) < 2:
            errors["fname"] = "First Name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirmPassword']:
            errors["passwordMatch"] = "Passwords should match"

        #email = self.cleaned_data.get('email')
        userList = User.objects.filter(email=postData['email'])
        if userList:
            errors["email"] ='This email address is already in use.'
        else:
            print("user does not exist")

        return errors


class ActivityManager(models.Manager):
    def activity_validator(self, postData):
    
        errors = {}
        if len(postData['title']) < 2:
            errors["title"] = "The title should be at least 2 characters"
        if int(postData["age"]) == -1:
            errors["age"] = "You need to select a age."
        if int(postData['category']) == -1 and len(postData['addNewCategory']) < 2:
            errors["category"] = "You need to select a category."
        if int(postData['category']) != -1 & len(postData['addNewCategory']) > 2:
            errors["category"] = "Please select a category or add a new category."
        # if len(postData['myfile']) == 0:
        #     errors["myfile"] = "Please add a photo."
        if len(postData['content']) < 10:
            errors["content"] = "The Content should be at least 10 characters"

        return errors

# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    isAdmin= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Category(models.Model):
    name= models.CharField(max_length=255)
    descrption= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Activity(models.Model):
    title= models.CharField(max_length=255)
    age = models.IntegerField(default=1)
    content= models.TextField()
    category = models.ForeignKey(Category, related_name="activities", on_delete = models.CASCADE)
    title_image_url = models.URLField(blank=True)
    document_url=models.URLField(null=True,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ActivityManager()


class Comment(models.Model):
    comment = models.TextField()
    activity = models.ForeignKey(Activity, related_name="activity_comments", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="user_comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


