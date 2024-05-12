# Generated by Django 5.0.6 on 2024-05-11 23:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('phone_number', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('code', models.CharField(max_length=8)),
                ('is_valid', models.BooleanField()),
                ('profile_picture', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
