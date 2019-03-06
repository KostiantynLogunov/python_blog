from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.jpg', upload_to='user_images')

    def __str__(self):
        return f'Profile of user {self.user.username}'

    def save(self):
        super(Profile, self).save()

        image = Image.open(self.img.path)

        if image.height > 64 or image.width > 64:
            resize = (64, 64)
            image.thumbnail(resize)
            image.save(self.img.path)