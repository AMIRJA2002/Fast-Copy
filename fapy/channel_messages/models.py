from django.db import models
from django.contrib.auth import get_user_model
from ..common.models import BaseModel as BM

User = get_user_model()


class Channel(BM):

    class ChannelType(models.TextChoices):
        private = 'private'
        public = 'public'

    type = models.CharField(max_length=10, default=ChannelType.private, choices=ChannelType.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_channels', db_index=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers_channels', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    topic = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'


class TextMessage(BM):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender_text_messages', null=True, blank=True)
    channels = models.ManyToManyField(Channel, related_name='channels_text_messages')
    text = models.TextField()

    def __str__(self):
        return f'{self.sender.id}->{self.text[:30]}'