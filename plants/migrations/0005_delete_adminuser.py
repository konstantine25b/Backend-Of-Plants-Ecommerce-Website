# Generated by Django 5.0.2 on 2024-03-17 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0004_alter_customuser_options_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdminUser',
        ),
    ]
