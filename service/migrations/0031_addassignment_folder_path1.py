# Generated by Django 4.2.6 on 2024-03-15 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0030_addassignment_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='addassignment',
            name='folder_path1',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
