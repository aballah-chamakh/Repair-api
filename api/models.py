from django.db import models
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


CITY_CHOICES = {
    ('city','City'),
    ('ariana','Ariana'),
    ('tunis','Tunis'),
    ('sfax','Sfax'),
    ('bizert','Bizert'),
    ('gafsa','Gafsa'),

}
CATEGORIE_CHOICES = {
    ('all categories','All categories'),
    ('web development','Web development'),
    ('web development','Web designe'),
}
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='defaultProfile.png')
    about = models.CharField(max_length=1000)
    phone = models.CharField(max_length=8)
    city = models.CharField(max_length=30,choices=CITY_CHOICES)
    def __str__(self):
        return 'profile : '+self.user.username


class Offer(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile_set')
    image = models.ImageField(default='default.jpg')
    title = models.CharField(max_length=550)
    description = models.CharField(max_length=1000)
    hide = models.BooleanField(default=False)
    categorie = models.CharField(max_length=30,choices=CATEGORIE_CHOICES)
    likes   = models.ManyToManyField(User,blank=True,related_name='offer_likes')
    def __str__ (self):
        return self.title+' from '+self.profile.user.username+' ( hided : '+str(self.hide)+')'
    class Meta :
        ordering=['-id']

class Comment(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Offer,on_delete=models.CASCADE,blank=True,null=True)
    content = models.TextField()
    likes   = models.ManyToManyField(User,blank=True,related_name='comment_likes')

    def __str__(self):
        owner = 'none'
        if (self.owner is not None):
            owner = self.owner.username
        return 'comment owned by '+owner

class CommentResponse(models.Model):
    comment  = models.ForeignKey(Comment,on_delete=models.CASCADE,blank=True,null=True)
    owner    = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    content  = models.TextField()
    likes   = models.ManyToManyField(User,blank=True,related_name='res_comment_likes')

    def __str__(self):
        owner = 'none'
        if (self.owner is not None):
            owner = self.owner.username
        return 'comment response owned by '+owner


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created :
        profile_obj = Profile.objects.create(user=instance)
