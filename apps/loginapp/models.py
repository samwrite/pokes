from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from django.contrib import messages
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
    def register(self,postData):
        result = {'status':True, 'error':[]}
        if not postData['name'] or postData['name'] < 3:
            result['status'] = False
            result['error'].append('Name must be at least 3 characters')
        if not postData['alias'] or postData['alias'] < 3:
            result['status'] = False
            result['error'].append('Alias must be at least 3 characters')
        if not postData['email'] or not EMAIL_REGEX.match(postData['email']):
            result['status'] = False
            result['error'].append('Must be a valid email')
        if not postData['password'] or postData['password'] < 8:
            result['status'] = False
            result['error'].append('Password must be at least 8 characters')
        if not postData['cpassword'] or postData['cpassword'] != postData['password']:
            result['status'] = False
            result['error'].append('Passwords must match')
        if result['status'] == True:
            if User.objects.filter(email = postData['email']):
                result['status'] = False
                result['error'].append('Email is already registered')
            elif User.objects.filter(alias = postData['alias']):
                result['status'] = False
                result['error'].append('Alias is already registered')
            else:
                password = postData['password'].encode('utf-8')
                hashedpw = bcrypt.hashpw(password,bcrypt.gensalt(12))
                User.objects.create(
                    name = postData['name'],
                    alias = postData['alias'],
                    email = postData['email'],
                    birth = postData['birth'],
                    password = hashedpw,
                )
        return result
    def login(self,postData, sessionData):
        user = User.objects.filter(email = postData['email'])
        if len(user) > 0:
            hashed = User.objects.get(email = postData['email']).password.encode('utf-8')
            password = postData['password'].encode('utf-8')
            if bcrypt.hashpw(password,hashed) == hashed:
                sessionData['id'] = User.objects.get(email = postData['email']).id
                return True
            else:
                return False

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birth = models.DateField()
    pokes = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()