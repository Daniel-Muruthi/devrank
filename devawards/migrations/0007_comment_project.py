# Generated by Django 3.2.8 on 2021-10-27 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devawards', '0006_alter_userprofile_userpic'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='devawards.project'),
        ),
    ]
