# Generated by Django 4.2.6 on 2024-01-12 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_login_admin_user_remove_login_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register_student',
            name='user',
        ),
    ]
