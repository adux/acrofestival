# Generated by Django 2.0.5 on 2018-10-04 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0003_auto_20181004_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Entrie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(choices=[('style1', 'Style 1'), ('style2', 'Style 2'), ('style3', 'Style 3'), ('style4', 'Style 4'), ('style5', 'Style 5')], max_length=8)),
                ('icon', models.CharField(choices=[('icon fa-home', 'Home'), ('icon fa-flag-checkered', 'Flag'), ('icon fa-fire', 'Fire'), ('icon fa-cutlery', 'Cutlery'), ('icon fa-cogs', 'Cogs'), ('icon fa-om', 'Om'), ('icon fa-magic', 'Magic')], max_length=25)),
                ('time', models.CharField(max_length=5)),
                ('title', models.CharField(max_length=30)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fest.Day')),
            ],
        ),
        migrations.RemoveField(
            model_name='days',
            name='entries',
        ),
        migrations.DeleteModel(
            name='Days',
        ),
        migrations.DeleteModel(
            name='Entries',
        ),
    ]
