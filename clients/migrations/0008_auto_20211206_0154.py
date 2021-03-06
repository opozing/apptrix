# Generated by Django 3.2.9 on 2021-12-05 22:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_alter_customuser_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_to', to=settings.AUTH_USER_MODEL)),
                ('user_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='was_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.AddConstraint(
            model_name='match',
            constraint=models.UniqueConstraint(fields=('user', 'user_like'), name='unique_match'),
        ),
    ]
