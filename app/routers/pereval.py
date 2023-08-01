from fastapi import APIRouter, HTTPException, Request

from app.db_connection import database
from app.logger import get_logger
from app.models.models import (coords_table, images_table, pereval_add_table,
                               users_table)
from app.models.schemas import PerevalPost, SubmitDataResponse

logger = get_logger()

router = APIRouter(tags=["SubmitData"])


@router.post("/SubmitData",
             summary="Отправка данных о перевале для обработки",
             response_model=SubmitDataResponse,
             description=
             """
Objective:
The 'submit_data' function is used to receive data about a mountain pass from a user, process it, and store it in a database. The function updates user information if the user already exists in the database, creates a new user if they do not exist, and creates a new entry for the mountain pass in the database.

Inputs:
- request: an instance of the 'PerevalPost' class, containing information about the mountain pass and the user who submitted the data.

Flow:
1. The function checks if the user who submitted the data already exists in the database.
2. If the user exists, their information is updated. If not, a new user is created.
3. The function creates a new entry in the 'coords' table of the database, containing the latitude, longitude, and height of the mountain pass.
4. The function creates a new entry in the 'pereval_add' table of the database, containing information about the mountain pass, the user who submitted the data, and the coordinates of the mountain pass.
5. The function creates new entries in the 'pereval_images' table of the database for each image submitted with the data.
6. The function returns a 'SubmitDataResponse' object with a status code, a message, and the ID of the new entry in the 'pereval_add' table.

Outputs:
- SubmitDataResponse object: an instance of the 'SubmitDataResponse' class, containing a status code, a message, and the ID of the new entry in the 'pereval_add' table.
             """, )
async def submit_data(request: PerevalPost):
    query = users_table.select().where(users_table.c.email == request.user.email)
    check_user = await database.fetch_one(query)

    if check_user:
        query = users_table.update().where(users_table.c.email == request.user.email). \
            values(first_name=request.user.name,
                   last_name=request.user.fam,
                   patronymic=request.user.otc,
                   phone=request.user.phone
                   )

        await database.execute(query)
        user = check_user.id

    else:
        query = users_table.insert().values(
            email=request.user.email,
            first_name=request.user.name,
            last_name=request.user.fam,
            patronymic=request.user.otc,
            phone=request.user.phone
        )

        user = await database.execute(query)

    query = coords_table.insert().values(latitude=request.coords.latitude,
                                         longitude=request.coords.longitude,
                                         height=request.coords.height)

    coords = await database.execute(query)

    query = pereval_add_table.insert().values(
        beauty_title=request.beauty_title,
        title=request.title,
        other_titles=request.other_titles,
        connect=request.connect,
        coords_id=coords,
        user_id=user,
        level_winter=request.level.winter,
        level_summer=request.level.summer,
        level_autumn=request.level.autumn,
        level_spring=request.level.spring
    )
    pereval = await database.execute(query)

    for image in request.images:
        query = images_table.insert().values(pereval=pereval,
                                             data=image.data,
                                             name=image.name)
        database.execute(query)

    return SubmitDataResponse(status=200, message="Отправлено успешно", id=pereval)
