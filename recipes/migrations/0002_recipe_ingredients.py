# Generated by Django 3.2.9 on 2023-05-09 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
