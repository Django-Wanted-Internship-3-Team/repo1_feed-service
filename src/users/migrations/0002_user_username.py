# Generated by Django 4.2.6 on 2023-10-27 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=1, max_length=128, unique=True),
            preserve_default=False,
        ),
    ]
