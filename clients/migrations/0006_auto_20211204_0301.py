# Generated by Django 3.2.9 on 2021-12-04 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20211203_0244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
