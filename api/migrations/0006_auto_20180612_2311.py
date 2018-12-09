# Generated by Django 2.0 on 2018-06-12 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180612_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='categorie',
            field=models.CharField(choices=[('web development', 'Web development'), ('categorie', 'Categorie'), ('web development', 'Web designe')], max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(choices=[('tunis', 'Tunis'), ('city', 'City'), ('sfax', 'Sfax'), ('bizert', 'Bizert'), ('ariana', 'Ariana')], max_length=30),
        ),
    ]