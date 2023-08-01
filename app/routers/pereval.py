from fastapi import APIRouter, Request, HTTPException

from app.db_connection import database
from app.models.models import users_table, coords_table, images_table, pereval_add_table
from app.models.schemas import PerevalPost, SubmitDataResponse
from app.logger import get_logger

logger = get_logger()

router = APIRouter(tags=["SubmitData"])


@router.post("/SubmitData",
             summary="Отправка данных о перевале для обработки",
             description="Отправка данных о перевале для обработки",
             response_model=SubmitDataResponse)
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
