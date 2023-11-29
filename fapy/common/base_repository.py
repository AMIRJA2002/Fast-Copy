from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from typing import Dict

User = get_user_model()


class BaseRepository:
    def __init__(self, model) -> None:
        self.model = model

    def get(self, dict_filter: Dict[str, any]) -> User:
        return get_object_or_404(self.model, **dict_filter)

    def save(self, obj):
        pass

    def create(self, data):
        return self.model.objects.create_user(**data)

    def update(self, obj):
        pass

    def filter(self, id):
        pass
