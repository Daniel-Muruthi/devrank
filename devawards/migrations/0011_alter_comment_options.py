# Generated by Django 3.2.8 on 2021-10-28 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devawards', '0010_alter_userprofile_userpic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('date',)},
        ),
    ]
