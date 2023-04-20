from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.png',upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()
        img = Image.open(self.profile_pic.path)
        if img.height > 640 or img.width > 640:
            output_size = (640,640)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
