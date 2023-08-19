from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

class Action(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True, related_name='target_obj')
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        indexes = [ 
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id']), 
        ]
        ordering = ['-created']
