# Generated by Django 2.0.7 on 2018-09-05 08:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0020_auto_20180905_0026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentlike',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commentlike',
            name='user',
        ),
        migrations.RemoveField(
            model_name='commentresponselike',
            name='ResComment',
        ),
        migrations.RemoveField(
            model_name='commentresponselike',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentresponse',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='res_comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(choices=[('sfax', 'Sfax'), ('tunis', 'Tunis'), ('bizert', 'Bizert'), ('city', 'City'), ('ariana', 'Ariana')], max_length=30),
        ),
        migrations.DeleteModel(
            name='CommentLike',
        ),
        migrations.DeleteModel(
            name='CommentResponseLike',
        ),
    ]