from django.contrib.auth import get_user_model
from dataclasses import dataclass

User = get_user_model()


@dataclass
class ChannelFilterBuilder:
    id: str = None
    type: bool = None
    owner: User = None
    topic: str = None

    def __post_init__(self):
        self.dict_filter = {}
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if value is not None:
                self.dict_filter[field] = value

    def get_dict_filter(self):
        return self.dict_filter
