# Generated by Django 3.2.8 on 2021-10-27 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devawards', '0008_remove_comment_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='devawards.project'),
        ),
    ]
