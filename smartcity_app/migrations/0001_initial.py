# Generated by Django 4.1.3 on 2022-11-17 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('ticket_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'images',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LoginInfo',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'login_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('created_timestamp', models.DateTimeField(blank=True, null=True)),
                ('days_remaining', models.IntegerField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('priority', models.CharField(blank=True, max_length=7, null=True)),
                ('state', models.CharField(blank=True, max_length=10, null=True)),
                ('technician', models.IntegerField(blank=True, null=True)),
                ('author', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'service_request',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceRequestComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=255, null=True)),
                ('created_timestamp', models.DateTimeField(blank=True, null=True)),
                ('ticket_id', models.IntegerField(blank=True, null=True)),
                ('author', models.IntegerField(blank=True, null=True)),
                ('request', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'service_request_comments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('state', models.CharField(blank=True, max_length=13, null=True)),
                ('created_timestamp', models.DateTimeField(blank=True, null=True)),
                ('priority', models.CharField(blank=True, max_length=7, null=True)),
                ('author', models.IntegerField(blank=True, null=True)),
                ('service_request', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ticket',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TicketComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=255, null=True)),
                ('created_timestamp', models.DateTimeField(blank=True, null=True)),
                ('ticket', models.IntegerField(blank=True, null=True)),
                ('author', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ticket_comments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('role', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
