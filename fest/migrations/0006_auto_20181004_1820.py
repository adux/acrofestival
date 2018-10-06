# Generated by Django 2.0.5 on 2018-10-04 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0005_auto_20181004_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrie',
            name='day',
        ),
        migrations.AddField(
            model_name='day',
            name='entrie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='day', to='fest.Entrie'),
            preserve_default=False,
        ),
    ]
