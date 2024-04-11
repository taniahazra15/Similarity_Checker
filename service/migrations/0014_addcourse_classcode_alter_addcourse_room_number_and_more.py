# Generated by Django 4.2.6 on 2024-01-04 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0013_remove_addstudent_courses_addstudent_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='addcourse',
            name='classcode',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addcourse',
            name='room_number',
            field=models.CharField(default=2, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addstudent',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
