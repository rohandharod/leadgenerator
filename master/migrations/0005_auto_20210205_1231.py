# Generated by Django 3.1.4 on 2021-02-05 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_auto_20210205_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rejectiontype',
            name='rejection_reason',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='rejectiontype',
            name='rejection_type',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='status',
            name='status',
            field=models.CharField(max_length=55),
        ),
    ]