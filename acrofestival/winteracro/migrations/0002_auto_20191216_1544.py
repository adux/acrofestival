# Generated by Django 2.0.5 on 2019-12-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winteracro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrie',
            name='icon',
            field=models.CharField(choices=[('icon fa-home', 'Home'), ('icon fa-flag-checkered', 'Flag'), ('icon fa-fire', 'Fire'), ('icon fa-utensils', 'Cutlery'), ('icon fa-cogs', 'Cogs'), ('icon fa-om', 'Om'), ('icon fa-snowflake', 'Snow'), ('icon fa-magic', 'Magic')], max_length=25),
        ),
    ]