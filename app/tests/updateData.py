import unittest
from unittest.mock import AsyncMock, patch
import pytest
from app.models.schemas import (CoordsModel, ImagesModel, LevelModel,
                                PatchResponse, PerevalPostRequest, UserModel)
from app.routers.submitdata import update_data


class TestUpdateData(unittest.TestCase):
    #  Tests that valid pereval_id and request data updates the pereval data and images
    @pytest.mark.asyncio
    async def test_valid_data(self):
        pereval_id = 1
        request = PerevalPostRequest(
            beauty_title='Beauty Title',
            title='Title',
            other_titles='Other Titles',
            connect='Connect',
            user=UserModel(
                email='email@example.com',
                fam='Fam',
                name='Name',
                otc='Otc',
                phone='Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3.0
            ),
            level=LevelModel(
                winter='Winter',
                summer='Summer',
                autumn='Autumn',
                spring='Spring'
            ),
            images=[ImagesModel(data=b'Image Data', name='Image Name')]
        )
        response = await update_data(pereval_id, request)
        assert response.state == 1
        assert response.message == 'Данные обновлены.'

    #  Tests that a non-existent pereval_id returns an error message
    @pytest.mark.asyncio
    async def test_nonexistent_pereval_id(self):
        pereval_id = 11111
        request = PerevalPostRequest(
            beauty_title='Beauty Title',
            title='Title',
            other_titles='Other Titles',
            connect='Connect',
            user=UserModel(
                email='email@example.com',
                fam='Fam',
                name='Name',
                otc='Otc',
                phone='Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3.0
            ),
            level=LevelModel(
                winter='Winter',
                summer='Summer',
                autumn='Autumn',
                spring='Spring'
            ),
            images=[ImagesModel(data=b'Image Data', name='Image Name')]
        )
        response = await update_data(pereval_id, request)
        assert response.state == 0
        assert response.message == 'Данные о перевале не найдены.'

    #  Tests that a pereval_id with non-'new' status returns an error message
    @pytest.mark.asyncio
    async def test_non_new_pereval_status(self):
        pereval_id = 2
        request = PerevalPostRequest(
            beauty_title='Beauty Title',
            title='Title',
            other_titles='Other Titles',
            connect='Connect',
            user=UserModel(
                email='email@example.com',
                fam='Fam',
                name='Name',
                otc='Otc',
                phone='Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3.0
            ),
            level=LevelModel(
                winter='Winter',
                summer='Summer',
                autumn='Autumn',
                spring='Spring'
            ),
            images=[ImagesModel(data=b'Image Data', name='Image Name')]
        )
        response = await update_data(pereval_id, request)
        assert response.state == 0
        assert response.message == 'Запрещено изменять проверенные данные.'

    #  Tests that mismatching user data in request and database returns an error message
    @pytest.mark.asyncio
    async def test_mismatching_user_data(self):
        pereval_id = 1
        request = PerevalPostRequest(
            beauty_title='Beauty Title',
            title='Title',
            other_titles='Other Titles',
            connect='Connect',
            user=UserModel(
                email='email@example.com',
                fam='Fam',
                name='Name',
                otc='Otc',
                phone='Different Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3.0
            ),
            level=LevelModel(
                winter='Winter',
                summer='Summer',
                autumn='Autumn',
                spring='Spring'
            ),
            images=[ImagesModel(data=b'Image Data', name='Image Name')]
        )
        response = await update_data(pereval_id, request)
        assert response.state == 0
        assert response.message == 'Запрещено изменять данные о пользователе.'

    #  Tests that an error updating pereval data returns an error message
    @pytest.mark.asyncio
    async def test_error_updating_pereval_data(self):
        pereval_id = 1
        request = PerevalPostRequest(
            beauty_title='Beauty Title',
            title='Title',
            other_titles='Other Titles',
            connect='Connect',
            user=UserModel(
                email='email@example.com',
                fam='Fam',
                name='Name',
                otc='Otc',
                phone='Phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3.0
            ),
            level=LevelModel(
                winter='Winter',
                summer='Summer',
                autumn='Autumn',
                spring='Spring'
            ),
            images=[ImagesModel(data=b'Image Data', name='Image Name')]
        )
        with patch('app.routes.update_pereval', side_effect=Exception):
            response = await update_data(pereval_id, request)
            assert response.state == 0
            assert response.message == 'Error update pereval'
