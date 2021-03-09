from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['email']) < 1:
            errors['email'] = "Please enter an email address"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"

        try:
            User.objects.get(email=postData['email'])
            errors['email'] = "Invalid email!"
        except:
            pass

        try:
            User.objects.get(username=postData['username'])
            errors['username'] = "Username already taken!"
        except:
            pass

        if len(postData['password']) < 1:
            errors['password'] = "Please enter a valid password"

        if postData['password'] != postData['confirm']:
            errors['password'] = "Passwords do not match"

        return errors

class User(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Beer(models.Model):
    brand = models.CharField(max_length=50)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    store = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
# state tag from many to many
    user = models.ManyToManyField(User, related_name="beer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
