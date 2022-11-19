# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Images(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    ticketid = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticketId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'images'


class LoginInfo(models.Model):
    email = models.CharField(primary_key=True, max_length=50)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'login_info'


class ServiceRequest(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    days_remaining = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    priority = models.CharField(max_length=7, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    technicianid = models.ForeignKey('User', models.DO_NOTHING, db_column='technicianId', blank=True, null=True, related_name='request_technician')  # Field name made lowercase.
    authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True, related_name='request_author')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'service_request'


class ServiceRequestComments(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    ticketid = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticketId', blank=True, null=True)  # Field name made lowercase.
    authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True)  # Field name made lowercase.
    requestid = models.ForeignKey(ServiceRequest, models.DO_NOTHING, db_column='requestId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'service_request_comments'


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=13, blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=7, blank=True, null=True)
    authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True)  # Field name made lowercase.
    service_request = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket'


class TicketComments(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    ticketid = models.ForeignKey(Ticket, models.DO_NOTHING, db_column='ticketId', blank=True, null=True)  # Field name made lowercase.
    authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ticket_comments'


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    role = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
