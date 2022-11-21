from django.db import models

# Create your models here.

class AdminInfo(models.Model):
    username = models.CharField(primary_key=True, max_length=5)
    password = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'admin_info'


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    role = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'