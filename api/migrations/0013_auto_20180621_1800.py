# Generated by Django 2.0 on 2018-06-21 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20180621_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='defaultProfile.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='offer',
            name='categorie',
            field=models.CharField(choices=[('web development', 'Web designe'), ('categorie', 'Categorie'), ('web development', 'Web development')], max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(choices=[('bizert', 'Bizert'), ('ariana', 'Ariana'), ('sfax', 'Sfax'), ('city', 'City'), ('tunis', 'Tunis')], max_length=30),
        ),
    ]
