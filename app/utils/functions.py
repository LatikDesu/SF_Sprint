from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import DatabaseError, IntegrityError

from app.db_connection import database
from app.logger import get_logger
from app.models.models import (coords_table, images_table, pereval_add_table,
                               users_table)
from app.models.schemas import (CoordsModel, ImagesModel, LevelModel,
                                PerevalGetResponse, PerevalPostRequest,
                                UserModel)

logger = get_logger()


async def get_or_create_coords(coords: CoordsModel, coords_id: Optional[int] = None) -> int:
    try:
        if coords_id:
            query = coords_table.select().where(coords_table.c.id == coords_id)
            check_coords = await database.fetch_one(query)
            if check_coords:
                query = coords_table.update().where(coords_table.c.id == coords_id). \
                    values(longitude=coords.longitude,
                           latitude=coords.latitude,
                           height=coords.height)

                await database.execute(query)
                logger.info(f"Coords updated successfully. ID: {coords_id}")
                return check_coords.id

        query = coords_table.insert().values(latitude=coords.latitude,
                                             longitude=coords.longitude,
                                             height=coords.height)
        coords_id = await database.execute(query)
        return coords_id

    except (DatabaseError, IntegrityError) as e:
        logger.error('Error creating coordinates: %s', str(e))
        raise HTTPException(status_code=500, detail='Error creating coordinates')


async def create_pereval(request: PerevalPostRequest, user_id: int, coords_id: int) -> int:
    try:
        query = pereval_add_table.insert().values(
            beauty_title=request.beauty_title,
            title=request.title,
            other_titles=request.other_titles,
            connect=request.connect,
            coords_id=coords_id,
            user_id=user_id,
            level_winter=request.level.winter,
            level_summer=request.level.summer,
            level_autumn=request.level.autumn,
            level_spring=request.level.spring
        )
        return await database.execute(query)
    except Exception as e:
        logger.error(f"Error creating pereval: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating pereval")


async def update_pereval(request: PerevalPostRequest, pereval_id: int, user_id: int, coords_id: int) -> int:
    try:
        query = pereval_add_table.update().where(pereval_add_table.c.id == pereval_id).values(
            beauty_title=request.beauty_title,
            title=request.title,
            other_titles=request.other_titles,
            connect=request.connect,
            coords_id=coords_id,
            user_id=user_id,
            level_winter=request.level.winter,
            level_summer=request.level.summer,
            level_autumn=request.level.autumn,
            level_spring=request.level.spring
        )

        return await database.execute(query)
    except Exception as e:
        logger.error(f"Error update pereval: {str(e)}")
        raise HTTPException(status_code=500, detail="Error update pereval")


async def get_or_create_user(user: UserModel) -> int:
    try:
        query = users_table.select().where(users_table.c.email == user.email)
        check_user = await database.fetch_one(query)

        if check_user:
            query = users_table.update().where(users_table.c.email == user.email). \
                values(first_name=user.name,
                       last_name=user.fam,
                       patronymic=user.otc,
                       phone=user.phone
                       )

            await database.execute(query)
            return check_user.id

        else:
            query = users_table.insert().values(
                email=user.email,
                first_name=user.name,
                last_name=user.fam,
                patronymic=user.otc,
                phone=user.phone
            )

            return await database.execute(query)
    except (DatabaseError, IntegrityError) as e:
        logger.error(f"Error getting or creating user: {str(e)}")


async def create_images(images: List[ImagesModel], pereval_id: int) -> None:
    try:
        values_list = [{'pereval': pereval_id, 'data': image.data, 'name': image.name} for image in images]
        query = images_table.insert()
        await database.execute_many(query, values_list)
    except (DatabaseError, IntegrityError) as e:
        logger.error(f"Error creating image: {str(e)}")


async def get_images(pereval_id: int) -> List[ImagesModel]:
    try:
        query = images_table.select().where(images_table.c.pereval == pereval_id)
        images = await database.fetch_all(query)
    except Exception as e:
        logger.error(f'Error retrieving images data: {e}')
        return []

    return [ImagesModel(**image) for image in images]


async def get_pereval_by_id(pereval):
    user = UserModel(
        email=pereval.email,
        fam=pereval.last_name,
        name=pereval.first_name,
        otc=pereval.patronymic,
        phone=pereval.phone
    )

    coords = CoordsModel(
        latitude=pereval.latitude,
        longitude=pereval.longitude,
        height=pereval.height
    )

    level = LevelModel(
        winter=pereval.level_winter,
        summer=pereval.level_summer,
        autumn=pereval.level_autumn,
        spring=pereval.level_spring
    )

    images = await get_images(pereval.id)

    return PerevalGetResponse(
        id=pereval.id,
        status=pereval.status,
        beauty_title=pereval.beauty_title,
        title=pereval.title,
        other_titles=pereval.other_titles,
        connect=pereval.connect,
        add_time=pereval.add_time,
        user=user,
        coords=coords,
        level=level,
        images=images
    )
