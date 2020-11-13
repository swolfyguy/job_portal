# Generated by Django 3.0.7 on 2020-11-10 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_salary',
            field=models.BigIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='type',
            field=models.CharField(choices=[('1', 'Full Time'), ('2', 'Part Time'), ('3', 'Intern')], max_length=20),
        ),
    ]