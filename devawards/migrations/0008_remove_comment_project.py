# Generated by Django 3.2.8 on 2021-10-27 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devawards', '0007_comment_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='project',
        ),
    ]