from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='rel_from_set')
    user_to = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [models.Index(fields=['-created'])]
        ordering = ['-created']
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'
    
# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, symmetrical=False, related_name='followers'))


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    
    def __str__(self):
        return f'Profile of {self.user.username}'