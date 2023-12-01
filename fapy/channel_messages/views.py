from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from ..channel_messages.data_trasfer.repository import ChannelRepository, RedisChannelRepository
from ..channel_messages.filter_builder import ChannelFilterBuilder
from ..channel_messages.models import Channel
from ..channel_messages.services import ChannelService, RedisChannel


class CreateChannelAPI(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Channel
            exclude = ('owner',)

    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Channel
            fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data = self.InputSerializer(data=data)
        data.is_valid(raise_exception=True)

        channel_service = ChannelService(repository=ChannelRepository)
        channel = channel_service.create_channel(data=data.data, user=request.user)

        return Response(self.OutPutSerializer(channel).data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        data = request.data.get('id', None)
        channel_service = ChannelService(
            repository=ChannelRepository
        ).get_channel(data=data, filter_builder=ChannelFilterBuilder, user=request.user)

        if data is not None:
            response = self.OutPutSerializer(channel_service).data
        elif data is None:
            response = self.OutPutSerializer(channel_service, many=True).data

        return Response(response, status=status.HTTP_200_OK)


class SubscriberChannelAPI(APIView):
    class InputSerializer(serializers.Serializer):
        topic = serializers.CharField(max_length=255)

    def get(self, request, *args, **kwargs):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        redis_channel = RedisChannel(repository=RedisChannelRepository, topic=data.data['topic'])
        redis_channel.get_channel(repository=ChannelRepository, filter_builder=ChannelFilterBuilder)
        redis_channel.subscribe_to_channel()
        return Response({'msg': 'subscribed to channel'})


class PublishMessageAPI(APIView):
    class InputSerializer(serializers.Serializer):
        message = serializers.CharField(max_length=1000)

    def post(self, request, *args, **kwargs):
        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        redis_channel = RedisChannel(repository=RedisChannelRepository, topic=data.data['message'])
        redis_channel.get_channel(repository=ChannelRepository, filter_builder=ChannelFilterBuilder)
        return Response({'msg': 'subscribed to channel'})
