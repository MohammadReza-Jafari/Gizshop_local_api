# Generated by Django 2.2 on 2020-07-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(editable=False, max_length=254, unique=True),
        ),
    ]
