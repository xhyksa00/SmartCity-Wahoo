# models.py
# Authors: Leopold Nemcek, Rudolf Hyksa
# Description:  File defining DB models used by the admin app
#               Classes describe tables in our database

from django.db import models


# Admin login info table
class AdminInfo(models.Model):
    username = models.CharField(primary_key=True, max_length=5)
    password = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'admin_info'

# User table
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    role = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'