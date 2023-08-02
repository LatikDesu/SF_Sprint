from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.validators import datetime


class UserModel(BaseModel):
    """ Model for user """
    email: EmailStr
    fam: str
    name: str
    otc: str
    phone: Optional[str] = 'Unknown'


class CoordsModel(BaseModel):
    """ Model for coordinates """
    latitude: float
    longitude: float
    height: int


class ImagesModel(BaseModel):
    """ Model for images """
    data: str
    name: str


class LevelModel(BaseModel):
    """ Model for level """
    winter: str
    summer: str
    autumn: str
    spring: str


class PerevalPostRequest(BaseModel):
    """    Model for post request to pereval add event"""

    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None

    user: UserModel
    coords: CoordsModel

    level: LevelModel

    images: list[ImagesModel]


class PerevalResponse(BaseModel):
    """ Model for post response to pereval add event"""

    status: int
    message: Optional[str] = None
    id: Optional[int] = None


class PatchResponse(BaseModel):
    """ Model for patch response to pereval patch event"""

    state: int
    message: Optional[str] = None


class PerevalGetResponse(BaseModel):
    """ Model for get response to pereval by id"""

    id: int
    status: str
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime

    user: UserModel
    coords: CoordsModel

    level: LevelModel

    images: list[ImagesModel]


class PerevalResponseByEmail(BaseModel):
    """ Model for get response to pereval by email"""

    perevals: list[PerevalGetResponse]
