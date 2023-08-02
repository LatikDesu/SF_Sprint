import sqlalchemy
from fastapi import APIRouter
from sqlalchemy.exc import DatabaseError, IntegrityError
from starlette.responses import JSONResponse

from app.db_connection import database
from app.logger import get_logger
from app.models.models import coords_table, pereval_add_table, users_table
from app.models.schemas import (PatchResponse, PerevalGetResponse,
                                PerevalPostRequest, PerevalResponse,
                                PerevalResponseByEmail)
from app.utils.functions import (create_images, create_pereval,
                                 get_or_create_coords, get_or_create_user,
                                 get_pereval_by_id, update_pereval)

logger = get_logger()

router = APIRouter(prefix="/SubmitData", tags=["SubmitData"])


@router.post("",
             summary="Отправка данных о перевале для обработки",
             description="Отправляет данные о перевале для обработки",
             response_model=PerevalResponse)
async def submit_data(request: PerevalPostRequest) -> PerevalResponse:
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


@router.get("",
            summary="Получение данных о перевале по id",
            description="Получение данных о перевале по id",
            response_model=PerevalGetResponse)
async def get_data(pereval_id: int):
    async with database.connection():
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
            return JSONResponse({'status': 500, 'message': "Ошибка при получении данных"})

        except Exception as e:
            logger.error(f"Error getting data: {str(e)}")
            return JSONResponse({'status': 500, 'message': "Ошибка при получении данных"})


@router.patch("",
              summary="Обновление данных о перевале",
              description="Обновление данных о перевале",
              response_model=PatchResponse)
async def update_data(pereval_id: int, request: PerevalPostRequest) -> PatchResponse:
    async with database.transaction():
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
            return PatchResponse(state=0, message='Данные о перевале не найдены.')

        if check_pereval.status != 'new':
            logger.error(f"Can not update data. Pereval ID: {pereval_id}")
            return PatchResponse(state=0, message='Запрещено изменять проверенные данные.')

        if check_pereval.email != request.user.email or check_pereval.last_name != request.user.fam or \
                check_pereval.first_name != request.user.name or check_pereval.patronymic != request.user.otc \
                or check_pereval.phone != request.user.phone:
            logger.error(f"Can not update user data. Pereval ID: {pereval_id}")
            return PatchResponse(state=0, message='Запрещено изменять данные о пользователе.')

        user = check_pereval.user_id
        coords = await get_or_create_coords(request.coords, check_pereval.coords_id)
        pereval = await update_pereval(request, pereval_id, user, coords)
        await create_images(request.images, pereval)

        logger.info(f"Data updated successfully.")

        return PatchResponse(state=1, message="Данные обновлены.")


@router.get("/<user_email>",
            summary="Получение данных о перевалах добавленных пользователем",
            description="Получение данных о перевалах добавленных пользователем",
            response_model=PerevalResponseByEmail)
async def get_data_by_email(user_email: str):
    async with database.connection():
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
                .where(users_table.c.email == user_email)
            )
            entities = await database.fetch_all(query)

            if entities:
                list_perevals = []
                for entity in entities:
                    try:
                        pereval = await get_pereval_by_id(entity)
                        list_perevals.append(pereval)
                    except Exception as e:
                        logger.error(f"Error getting data: {str(e)}")
                        continue
                return PerevalResponseByEmail(perevals=list_perevals)

            return JSONResponse({'status': 204, 'message': 'Данные не найдены.'})

        except (DatabaseError, IntegrityError) as e:
            logger.error(f"Error getting data: {str(e)}")
            return JSONResponse({'status': 500, 'message': "Ошибка при получении данных"})

        except Exception as e:
            logger.error(f"Error getting data: {str(e)}")
            return JSONResponse({'status': 500, 'message': "Ошибка при получении данных"})
