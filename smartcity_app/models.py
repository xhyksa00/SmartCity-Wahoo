# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models


# class Images(models.Model):
#     name = models.CharField(primary_key=True, max_length=50)
#     ticketid = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticketId', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'images'


# class LoginInfo(models.Model):
#     email = models.CharField(primary_key=True, max_length=50)
#     userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
#     password = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'login_info'


# class ServiceRequest(models.Model):
#     id = models.AutoField(primary_key=True)
#     description = models.CharField(max_length=255)
#     created_timestamp = models.DateTimeField(blank=True, null=True)
#     days_remaining = models.IntegerField(blank=True, null=True)
#     price = models.IntegerField(blank=True, null=True)
#     priority = models.CharField(max_length=7, blank=True, null=True)
#     state = models.CharField(max_length=10, blank=True, null=True)
#     technicianid = models.ForeignKey('User', models.DO_NOTHING, db_column='technicianId', blank=True, null=True, related_name='request_technician')  # Field name made lowercase.
#     authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True, related_name='request_author')  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'service_request'


# class ServiceRequestComments(models.Model):
#     id = models.AutoField(primary_key=True)
#     text = models.CharField(max_length=255, blank=True, null=True)
#     created_timestamp = models.DateTimeField(blank=True, null=True)
#     ticketid = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticketId', blank=True, null=True)  # Field name made lowercase.
#     authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True)  # Field name made lowercase.
#     requestid = models.ForeignKey(ServiceRequest, models.DO_NOTHING, db_column='requestId', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'service_request_comments'


# class Ticket(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=50)
#     description = models.CharField(max_length=255)
#     state = models.CharField(max_length=13, blank=True, null=True)
#     created_timestamp = models.DateTimeField(blank=True, null=True)
#     priority = models.CharField(max_length=7, blank=True, null=True)
#     authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True)  # Field name made lowercase.
#     service_request = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'ticket'


# class TicketComments(models.Model):
#     id = models.AutoField(primary_key=True)
#     text = models.CharField(max_length=255, blank=True, null=True)
#     created_timestamp = models.DateTimeField(blank=True, null=True)
#     ticketid = models.ForeignKey(Ticket, models.DO_NOTHING, db_column='ticketId', blank=True, null=True)  # Field name made lowercase.
#     authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'ticket_comments'


# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20)
#     surname = models.CharField(max_length=20)
#     role = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'user'


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminInfo(models.Model):
    username = models.CharField(primary_key=True, max_length=5)
    password = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'admin_info'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Images(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    ticketid = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticketId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'images'


class LoginInfo(models.Model):
    email = models.CharField(primary_key=True, max_length=50)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'login_info'


class ServiceRequest(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    days_remaining = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    priority = models.CharField(max_length=7)
    state = models.CharField(max_length=11, blank=True, null=True)
    ticketid = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticketId', blank=True, null=True)  # Field name made lowercase.
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
    state = models.CharField(max_length=17, blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=7)
    authorid = models.ForeignKey('User', models.DO_NOTHING, db_column='authorId', blank=True, null=True)  # Field name made lowercase.

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
