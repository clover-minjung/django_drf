from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # profile = models.OneToOneField('Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='user_profile')
    # profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/df.jpg')
    bio = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.username
    
# class Profile(models.Model):
#     signup_date = models.DateTimeField(auto_now_add=True)
#     birthday = models.DateField(null=True, blank=True)
#     website = models.URLField(blank=True)
#     country = models.CharField(max_length=100, blank=True)
#     address = models.TextField(blank=True)

#     def __str__(self):
#         return self.signup_date