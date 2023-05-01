# Generated by Django 4.2 on 2023-04-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='writing_time',
            new_name='created_time',
        ),
        migrations.RemoveField(
            model_name='review',
            name='evaluation',
        ),
        migrations.RemoveField(
            model_name='review',
            name='review_text',
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='review',
            name='review',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='review',
            name='subject',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='updated_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
