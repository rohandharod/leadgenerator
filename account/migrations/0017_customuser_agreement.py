# Generated by Django 3.1.4 on 2021-02-02 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20210104_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='agreement',
            field=models.FileField(default=2, upload_to='agreements'),
            preserve_default=False,
        ),
    ]
