# Generated by Django 3.2.3 on 2021-06-11 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_remove_item_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeactivity',
            old_name='Employee',
            new_name='employee',
        ),
    ]
