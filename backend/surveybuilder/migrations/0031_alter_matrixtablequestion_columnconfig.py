# Generated by Django 3.2.7 on 2023-05-11 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveybuilder', '0030_alter_matrixtablequestion_columnconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrixtablequestion',
            name='columnConfig',
            field=models.TextField(blank=True, default='[{"label":"Strong disgree","value":"e"},{"label":"Disagree","value":"d"},{"label":"Neutral","value":"c"},{"label":"Agree","value":"b"},{"label":"Strong agree","value":"a"}]', max_length=5000),
        ),
    ]
