from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from typing import Dict


User = get_user_model()


class BaseRepository:
    def __init__(self, model) -> None:
        self.model = model

    def get(self, dict_filter: Dict[str, any]) -> QuerySet:
        return get_object_or_404(self.model, **dict_filter)

    def save(self, obj):
        pass

    def create(self, data) -> QuerySet:
        return self.model.objects.create(**data)

    def update(self, obj):
        pass

    def filter(self, dict_filter: Dict[str, any]) -> QuerySet:
        return self.model.objects.filter(**dict_filter)
