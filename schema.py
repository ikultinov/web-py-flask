import pydantic
from typing import Optional, Type


class CreateAdvertisement(pydantic.BaseModel):
    article: str
    description: Optional[str]
    owner: str


class PatchAdvertisement(pydantic.BaseModel):
    article: Optional[str]
    description: Optional[str]
    owner: Optional[str]


VALIDATION_CLASS = Type[CreateAdvertisement] | Type[PatchAdvertisement]