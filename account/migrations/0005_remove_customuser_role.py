# Generated by Django 3.1.2 on 2020-11-02 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
    ]