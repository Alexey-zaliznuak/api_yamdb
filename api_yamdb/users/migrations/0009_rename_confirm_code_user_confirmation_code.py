# Generated by Django 3.2 on 2023-03-09 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='confirm_code',
            new_name='confirmation_code',
        ),
    ]