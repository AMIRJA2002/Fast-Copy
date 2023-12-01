from ...common.base_repository import BaseRepository
from ...common.redis_connection import RedisConnection
from ..models import Channel


class RedisChannelRepository(RedisConnection):
    def subscribe(self, topic):
        conn = self.connection()
        sub = conn.pubsub()
        sub.subscribe(topic)
        return sub

    def _publish(self, topic, message):
        conn = self.connection()
        conn.pubsub(topic, message)


class ChannelRepository(BaseRepository):
    def __init__(self, model: Channel = Channel) -> None:
        self.model = model
        super(ChannelRepository, self).__init__(self.model)



