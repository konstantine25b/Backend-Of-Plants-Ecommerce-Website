# Generated by Django 5.0.2 on 2024-04-04 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_review_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='username',
            field=models.CharField(max_length=150),
        ),
    ]
