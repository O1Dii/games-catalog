# Generated by Django 2.2.1 on 2019-06-10 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20190610_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamemodel',
            name='summary',
            field=models.CharField(max_length=2500, null=True),
        ),
    ]