from django.db import models
import django.contrib.auth.hashers as hasher
import os

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=15, blank=False)
    password = models.CharField(max_length=20, blank=False)


    def __str__(self):
        return str(self.username)
    
    def encryptPassword(self, password):
        salt = os.urandom(16)
        
        hashedPassword = hasher.make_password(password, salt=salt, hasher='argon2')

        return hashedPassword
    