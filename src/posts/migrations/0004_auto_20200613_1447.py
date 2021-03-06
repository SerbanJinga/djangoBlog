# Generated by Django 3.0.7 on 2020-06-13 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200613_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header1',
            field=models.CharField(default=True, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='header2',
            field=models.CharField(default=True, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph1',
            field=models.TextField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph2',
            field=models.TextField(default=True),
            preserve_default=False,
        ),
    ]
