# Generated by Django 2.1.1 on 2018-12-13 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sentSMSLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=13)),
                ('message_sent', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('registration code', 'registration code'), ('password reset code', 'password reset code')], max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Sent SMS',
                'verbose_name_plural': 'Sent SMS',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='userActivities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('mobile_number', models.CharField(max_length=13)),
                ('action', models.CharField(choices=[('user_registration', 'user_registration'), ('reset_password', 'reset_password'), ('change_password', 'change_password'), ('create_chama', 'create_chama'), ('update_chama', 'update_chama'), ('choose_plan', 'choose_plan'), ('change_plan', 'change_plan')], max_length=255)),
                ('token', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('in_progress', 'in_progress'), ('suspended', 'suspended'), ('completed', 'completed')], max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('state_changed_on', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
                'ordering': ['-state_changed_on'],
            },
        ),
    ]
