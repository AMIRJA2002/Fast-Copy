from django.core.exceptions import BadRequest
from django.db.models import QuerySet
from django.http import Http404

from .filter_builder import ChannelFilterBuilder
from ..channel_messages.models import Channel
from django.contrib.auth import get_user_model
from typing import Dict


User = get_user_model()


class RedisChannel:
    def __init__(self, repository, topic: str) -> None:
        self.repository = repository()
        self.topic = topic

    def subscribe_to_channel(self):
        sub = self.repository.subscribe(topic=self.topic)
        for message in sub.listen():
            print(message)

    def publish_to_channel(self, message: str):
        self.repository.publish(topic=self.topic, message=message)

    def get_channel(self, repository, filter_builder):
        dict_filter = filter_builder(topic=self.topic)
        return repository().get(dict_filter=dict_filter.get_dict_filter())


class ChannelService:
    def __init__(self, repository) -> None:
        self.repository = repository()

    def create_channel(self, data: Dict[str, any], user: User) -> Channel:
        data = data.copy()
        subscribers = data.pop('subscribers', None)
        data.update({'owner': user})
        channel = self.repository.create(data=data)
        if subscribers is not None:
            channel.subscribers.set(subscribers)
            channel.save()
        return channel

    def get_channel(self, filter_builder, user: User, data: int = None) -> Channel | QuerySet[Channel]:
        if data:
            dict_filter = filter_builder(owner=user, id=data)
            channel = self.repository.get(dict_filter=dict_filter.get_dict_filter())
        else:
            dict_filter = filter_builder(owner=user)
            channel = self.repository.filter(dict_filter=dict_filter.get_dict_filter())
        return channel
