# Generated by Django 2.1.7 on 2019-03-26 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]