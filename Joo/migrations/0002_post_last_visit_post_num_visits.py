# Generated by Django 4.1.7 on 2023-05-03 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Joo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='last_visit',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='num_visits',
            field=models.IntegerField(default=0),
        ),
    ]