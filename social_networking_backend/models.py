from django.db import models
from django.contrib.auth.models import User
from .enums import SATTUS_CHOICES


class BaseModel(models.Model):
    """
    Base class for all model classes
    """

    created_at = models.DateTimeField(
        auto_now_add=True, blank=False, help_text="Creation At")
    modified_at = models.DateTimeField(
        auto_now=True, blank=False, help_text="Updated At")

    class Meta:
        abstract = True


class FriendRequest(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friends = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    request_count = models.IntegerField(default=0)
    status = models.CharField(choices=SATTUS_CHOICES,
                              max_length=2, default='S')

    class Meta:
        ordering = ('-created_at',)
