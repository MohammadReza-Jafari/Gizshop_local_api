# Generated by Django 2.2 on 2020-08-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20200830_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maincategory',
            name='title',
            field=models.CharField(error_messages={'unique': 'این دسته بندی هم اکنون موجود می باشد'}, max_length=256, unique=True),
        ),
    ]
