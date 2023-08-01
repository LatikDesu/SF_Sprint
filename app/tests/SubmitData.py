# Dependencies:
# pip install pytest-mock
import pytest
from fastapi import HTTPException

from app.db_connection import database
from app.models.schemas import (CoordsModel, ImagesModel, LevelModel,
                                PerevalPost, UserModel)
from app.routers.pereval import submit_data


class TestSubmitData:
    #  Tests that valid input data is submitted successfully
    @pytest.mark.asyncio
    async def test_valid_input_data(self, mocker):
        request = PerevalPost(
            beauty_title='Test Beauty Title',
            title='Test Title',
            other_titles='Test Other Titles',
            connect='Test Connect',
            user=UserModel(
                email='test@test.com',
                fam='Test Fam',
                name='Test Name',
                otc='Test Otc',
                phone='Test Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3
            ),
            level=LevelModel(
                winter='Test Winter',
                summer='Test Summer',
                autumn='Test Autumn',
                spring='Test Spring'
            ),
            images=[ImagesModel(data='Test Data', name='Test Name')]
        )
        mocker.patch('app.routers.submit_data.database', database)
        mocker.patch('app.routers.submit_data.images_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.pereval_add_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.coords_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.select', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.update', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.insert', return_value=1)
        result = await submit_data(request)
        assert result.status == 200
        assert result.message == 'Отправлено успешно'
        assert result.id == 1

    #  Tests that user already in the database is updated successfully
    @pytest.mark.asyncio
    async def test_existing_user(self, mocker):
        request = PerevalPost(
            beauty_title='Test Beauty Title',
            title='Test Title',
            other_titles='Test Other Titles',
            connect='Test Connect',
            user=UserModel(
                email='test@test.com',
                fam='Test Fam',
                name='Test Name',
                otc='Test Otc',
                phone='Test Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3
            ),
            level=LevelModel(
                winter='Test Winter',
                summer='Test Summer',
                autumn='Test Autumn',
                spring='Test Spring'
            ),
            images=[ImagesModel(data='Test Data', name='Test Name')]
        )
        mocker.patch('app.routers.submit_data.database', database)
        mocker.patch('app.routers.submit_data.images_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.pereval_add_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.coords_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.select', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.update', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.insert', return_value=1)
        result = await submit_data(request)
        assert result.status == 200
        assert result.message == 'Отправлено успешно'
        assert result.id == 1

    #  Tests that new user is added to the database successfully
    @pytest.mark.asyncio
    async def test_new_user(self, mocker):
        request = PerevalPost(
            beauty_title='Test Beauty Title',
            title='Test Title',
            other_titles='Test Other Titles',
            connect='Test Connect',
            user=UserModel(
                email='test@test.com',
                fam='Test Fam',
                name='Test Name',
                otc='Test Otc',
                phone='Test Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3
            ),
            level=LevelModel(
                winter='Test Winter',
                summer='Test Summer',
                autumn='Test Autumn',
                spring='Test Spring'
            ),
            images=[ImagesModel(data='Test Data', name='Test Name')]
        )
        mocker.patch('app.routers.submit_data.database', database)
        mocker.patch('app.routers.submit_data.images_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.pereval_add_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.coords_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.select', return_value=None)
        mocker.patch('app.routers.submit_data.users_table.update', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.insert', return_value=1)
        result = await submit_data(request)
        assert result.status == 200
        assert result.message == 'Отправлено успешно'
        assert result.id == 1

    #  Tests that invalid input data is not submitted
    @pytest.mark.asyncio
    async def test_invalid_input_data(self, mocker):
        request = PerevalPost(
            beauty_title='Test Beauty Title',
            title='Test Title',
            other_titles='Test Other Titles',
            connect='Test Connect',
            user=UserModel(
                email='test@test.com',
                fam='Test Fam',
                name='Test Name',
                otc='Test Otc',
                phone='Test Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3
            ),
            level=LevelModel(
                winter='Test Winter',
                summer='Test Summer',
                autumn='Test Autumn',
                spring='Test Spring'
            ),
            images=[ImagesModel(data='Test Data', name='Test Name')]
        )
        mocker.patch('app.routers.submit_data.database', database)
        mocker.patch('app.routers.submit_data.images_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.pereval_add_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.coords_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.select', return_value=None)
        mocker.patch('app.routers.submit_data.users_table.update', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.insert', return_value=1)
        request.user.email = None
        with pytest.raises(HTTPException):
            await submit_data(request)

    #  Tests that user email is required
    @pytest.mark.asyncio
    async def test_missing_user_email(self, mocker):
        request = PerevalPost(
            beauty_title='Test Beauty Title',
            title='Test Title',
            other_titles='Test Other Titles',
            connect='Test Connect',
            user=UserModel(
                email=None,
                fam='Test Fam',
                name='Test Name',
                otc='Test Otc',
                phone='Test Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3
            ),
            level=LevelModel(
                winter='Test Winter',
                summer='Test Summer',
                autumn='Test Autumn',
                spring='Test Spring'
            ),
            images=[ImagesModel(data='Test Data', name='Test Name')]
        )
        mocker.patch('app.routers.submit_data.database', database)
        mocker.patch('app.routers.submit_data.images_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.pereval_add_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.coords_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.select', return_value=None)
        mocker.patch('app.routers.submit_data.users_table.update', return_value=1)
        mocker.patch('app.routers.submit_data.users_table.insert', return_value=1)
        with pytest.raises(HTTPException):
            await submit_data(request)
