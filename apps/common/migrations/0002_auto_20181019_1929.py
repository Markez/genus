# Generated by Django 2.1.1 on 2018-10-19 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentsmslogs',
            name='category',
            field=models.CharField(choices=[('Registration code', 'Registration code'), ('Password reset code', 'Password reset code')], max_length=200),
        ),
    ]
