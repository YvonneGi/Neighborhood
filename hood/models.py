from django.db import models
from django.contrib.auth.models import User
# from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField

# Create your models here.
class Profile(models.Model):
    profile_pic = models.ImageField(upload_to='photos/',null=True)
    fullname = models.CharField(max_length=255,null=True)
    username = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = HTMLField(null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.username.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
       if created:
           Profile.objects.create(username=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
       instance.profile.save()

    @classmethod
    def search_profile(cls,search_term):
        profiles = cls.objects.filter(fullname__icontains=search_term )
        return profiles


    def update_profile(self):

        ''' Method to update a profile in the database'''

        self.update()

    def delete_profile(self):

        ''' Method to delete a profile from the database'''

        self.delete()

