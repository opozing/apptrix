# Generated by Django 3.2.9 on 2021-12-05 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_auto_20211204_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(upload_to='avatars/'),
        ),
    ]
