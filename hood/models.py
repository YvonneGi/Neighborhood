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

class Neighborhood(models.Model):
    location = models.CharField(max_length=30, default="e.g Kigali, Byumba, Kibungo etc")
    name = models.CharField(max_length=30)
    occupants_count = models.IntegerField(default=0, blank=True)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hoods', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    '''
    this is added to ensure the linter has no errors saying class has no objects member in VS Code IDE
    '''
    objects = models.Manager()

    @classmethod
    def search_neighborhood_by_name(cls, search_term):
        neighborhoods = cls.objects.filter(name__icontains=search_term)
        return neighborhoods

    @classmethod
    def one_neighborhood(cls, id):
        neighborhood = Neighborhood.objects.filter(id=id)
        return neighborhood

    @classmethod
    def all_neighborhoods(cls):
        neighborhoods = cls.objects.all()
        return neighborhoods

    @classmethod
    def get_neighborhood_by_id(cls, id):
        neighborhood = Neighborhood.objects.filter(id=Neighborhood.id)
        return neighborhood

    @classmethod
    def get_all_profiles(cls):
        profile = Profile.objects.all()
        return profile


    def update_neighborhood(self):

        ''' Method to update a neighborhood in the database'''

        self.update()

    def delete_neighborhood(self):

        ''' Method to delete a neighborhood from the database'''

        self.delete()


class Business(models.Model):
    name = models.CharField(max_length=30)
    description = HTMLField(blank=True)
    email = models.EmailField(max_length=70, blank=True)
    biz_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    biz_hood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='biz', null=True)

    '''
    this is added to ensure the linter has no errors saying class has no objects member in VS Code IDE
    '''
    objects = models.Manager()

    @classmethod
    def search_by_name(cls, search_term):
        businesses = cls.objects.filter(name__icontains=search_term)
        return businesses

    @classmethod
    def get_neighborhood_businesses(cls, neighborhood_id):
        businesses = Business.objects.filter(neighborhood_id=id)
        return businesses

    @classmethod
    def get_hood_biz(cls, biz_hood):
        businesses = Business.objects.filter(biz_hood_pk=biz_hood)
        return businesses

    @classmethod
    def get_profile_businesses(cls, profile):
        businesses = Business.objects.filter(biz_owner__pk=profile)
        return businesses


    def update_business(self):

        ''' Method to update a business in the database'''

        self.update()

    def delete_business(self):

        ''' Method to delete a business from the database'''

        self.delete()

class Join(models.Model):
    '''
    Updating user location each time they join or leave a neghborhood	
    '''
    user_id = models.OneToOneField(User)
    hood_id = models.ForeignKey(Neighborhood)

    def __str__(self):
        return self.user_id

class Post(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/', blank=True)
    description = HTMLField(blank=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_hood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    '''
    this is added to ensure the linter has no errors saying class has no objects member in VS Code IDE
    '''
    objects = models.Manager()

    @classmethod
    def search_post(cls, search_term):
        posts = cls.objects.filter(name__icontains=search_term)
        return posts

    @classmethod
    def get_hood_posts(cls, post_hood):
        posts = Post.objects.filter(post_hood=id)
        return posts

    @classmethod
    def search_by_name(cls, search_term):
        posts = cls.objects.filter(name__icontains=search_term)
        return posts

    @classmethod
    def all_posts(cls,id):
        posts = Post.objects.all()
        return posts


