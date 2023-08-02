import sqlalchemy
from fastapi import APIRouter
from sqlalchemy.exc import DatabaseError, IntegrityError
from starlette.responses import JSONResponse

from app.db_connection import database
from app.logger import get_logger
from app.models.models import pereval_add_table, coords_table, users_table
from app.models.schemas import PerevalPostRequest, PerevalResponse, PerevalGetResponse, PatchResponse
from app.utils.functions import get_or_create_coords, create_images, create_pereval, get_or_create_user, \
    get_pereval_by_id

logger = get_logger()

router = APIRouter(prefix="/SubmitData", tags=["SubmitData"])


@router.post("",
             summary="Отправка данных о перевале для обработки",
             description="Отправляет данные о перевале для обработки",
             response_model=PerevalResponse)
async def submit_data(request: PerevalPostRequest):
    async with database.transaction():
        try:
            user = await get_or_create_user(request.user)
            coords = await get_or_create_coords(request.coords)
            pereval = await create_pereval(request, user, coords)
            await create_images(request.images, pereval)

            logger.info(f"Data submitted successfully. Pereval ID: {pereval}")

            return PerevalResponse(status=200, message="Отправлено успешно", id=pereval)

        except (DatabaseError, IntegrityError) as e:
            logger.error(f"Error submitting data: {str(e)}")
            return PerevalResponse(status=500, message=str(e))

        except Exception as e:
            logger.error(f"Error submitting data: {str(e)}")
            return PerevalResponse(status=500, message="Ошибка при отправке данных")


@router.post("/<pereval_id>",
             summary="Получение данных о перевале по id",
             description="Получение данных о перевале по id",
             response_model=PerevalGetResponse)
async def get_data(pereval_id: int):
    async with database.transaction():
        try:
            query = (
                sqlalchemy.select(
                    pereval_add_table,
                    coords_table,
                    users_table
                )
                .select_from(
                    pereval_add_table
                    .join(coords_table, pereval_add_table.c.coords_id == coords_table.c.id)
                    .join(users_table, pereval_add_table.c.user_id == users_table.c.id)
                )
                .where(pereval_add_table.c.id == pereval_id)
            )
            pereval = await database.fetch_one(query)

            if pereval:
                logger.info(f"Data retrieved successfully. Pereval ID: {pereval.id}")
                response = await get_pereval_by_id(pereval)
                return response

            else:
                logger.info(f"Data not found. Pereval ID: {pereval}")
                return JSONResponse({'status': 204, 'message': 'Данные не найдены.'})

        except (DatabaseError, IntegrityError) as e:
            logger.error(f"Error getting data: {str(e)}")
            return JSONResponse({'status': 500, 'message': str(e)})

        except Exception as e:
            logger.error(f"Error getting data: {str(e)}")
            return JSONResponse({'status': 500, 'message': "Ошибка при получении данных"})


@router.patch("",
              summary="Обновление данных о перевале",
              description="Обновление данных о перевале",
              response_model=PatchResponse)
async def update_data(pereval_id: int, request: PerevalPostRequest):
    async with database.transaction():
        try:
            query = (
                sqlalchemy.select(
                    pereval_add_table,
                    users_table
                )
                .select_from(
                    pereval_add_table
                    .join(users_table, pereval_add_table.c.user_id == users_table.c.id)
                )
                .where(pereval_add_table.c.id == pereval_id)
            )
            check_pereval = await database.fetch_one(query)

            if check_pereval is None:
                logger.info(f"Data not found. Pereval ID: {pereval_id} exists.")
                return JSONResponse({'state': 0, 'message': 'Данные о перевале не найдены.'})
            else:
                if check_pereval.status != 'new':
                    logger.info(f"Can not update data. Pereval ID: {pereval_id}")
                    return JSONResponse({'state': 0, 'message': 'Запрещено изменять проверенные данные.'})

                if check_pereval.email != request.user.email:
                    logger.info(f"Can not update user data. Pereval ID: {pereval_id}")
                    return JSONResponse({'state': 0, 'message': 'Запрещено изменять данные о другом пользователе.'})

                user = check_pereval.user.id
                coords = await get_or_create_coords(request.coords)
                pereval = await create_pereval(request, user, coords)
                await create_images(request.images, pereval)

                logger.info(f"Data submitted successfully. Pereval ID: {pereval}")

                return PerevalResponse(status=200, message="Отправлено успешно", id=pereval)



        except (DatabaseError, IntegrityError) as e:
            logger.error(f"Error getting data: {str(e)}")
            return JSONResponse({'state': 0, 'message': str(e)})

        except Exception as e:
            logger.error(f"Error getting data: {str(e)}")
            return JSONResponse({'state': 0, 'message': "Ошибка при получении данных"})