# Generated by Django 4.2.10 on 2024-03-03 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_userrecord_previous_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecord',
            name='previous_first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='previous_section',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='previous_student_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]