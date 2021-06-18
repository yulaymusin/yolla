# Generated by Django 3.2 on 2021-06-13 11:25

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'A participant with that username already exists.'}, help_text='Required. Used for log in paired with a password. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=50, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Username')),
                ('name', models.CharField(error_messages={'unique': 'Another participant signs opinions with this name.'}, help_text='Required. Used for signing opinions. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=50, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Name')),
                ('email', models.EmailField(help_text='Required. Used for password recovery.', max_length=254, verbose_name='Email address')),
                ('time_zone', models.CharField(default='UTC', max_length=50, verbose_name='Time zone')),
                ('l1', models.CharField(choices=[('en', 'English'), ('zh-hans', '简体中文'), ('zh-hant', '繁體中文'), ('es', 'Español'), ('ar', 'العربيّة'), ('fr', 'Français'), ('ru', 'Русский')], default='en', max_length=20, verbose_name='Primary language')),
                ('l2', models.CharField(blank=True, choices=[('en', 'English'), ('zh-hans', '简体中文'), ('zh-hant', '繁體中文'), ('es', 'Español'), ('ar', 'العربيّة'), ('fr', 'Français'), ('ru', 'Русский')], max_length=20, verbose_name='Secondary language')),
                ('about', models.TextField(blank=True, default='', verbose_name='About')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'participant',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
