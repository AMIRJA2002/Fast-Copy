from dataclasses import dataclass


@dataclass
class UserFilterBuilder:
    id: str = None
    is_active: bool = None
    phone_number: str = None

    def __post_init__(self):
        self.dict_filter = {}
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if value is not None:
                self.dict_filter[field] = value

    def get_dict_filter(self):
        return self.dict_filter
