import unittest
import pytest
from app.models.schemas import (CoordsModel, ImagesModel, LevelModel,
                                PerevalPostRequest, UserModel)
from app.routers.submitdata import submit_data


class TestSubmitData(unittest.TestCase):
    #  Tests that valid data is submitted successfully and a pereval ID is returned
    @pytest.mark.asyncio
    async def test_valid_data(self):
        request = PerevalPostRequest(
            beauty_title='Test Beauty Title',
            title='Test Title',
            user=UserModel(
                email='test@test.com',
                name='Test',
                fam='User',
                otc='Testovich',
                phone='+123456789'
            ),
            coords=CoordsModel(
                latitude=55.7522,
                longitude=37.6156,
                height=0
            ),
            level=LevelModel(
                winter=1,
                summer=2,
                autumn=3,
                spring=4
            ),
            images=[ImagesModel(data=b'123', name='test.jpg')]
        )

        response = await submit_data(request)
        assert response.status == 200
        assert response.message == 'Отправлено успешно'
        assert response.id is not None

    #  Tests that data with optional fields is submitted successfully and a pereval ID is returned
    @pytest.mark.asyncio
    async def test_optional_fields(self):
        request = PerevalPostRequest(
            beauty_title='Test Beauty Title',
            title='Test Title',
            user=UserModel(
                email='test@test.com',
                name='Test',
                fam='User',
                otc='Testovich',
                phone='+123456789'
            ),
            coords=CoordsModel(
                latitude=55.7522,
                longitude=37.6156,
                height=0
            ),
            level=LevelModel(
                winter=1,
                summer=2,
                autumn=3,
                spring=4
            ),
            images=[ImagesModel(data=b'123', name='test.jpg')],
            other_titles='Test Other Titles',
            connect='Test Connect'
        )
        response = await submit_data(request)
        assert response.status == 200
        assert response.message == 'Отправлено успешно'
        assert response.id is not None

    #  Tests that data with multiple images is submitted successfully and a pereval ID is returned
    @pytest.mark.asyncio
    async def test_multiple_images(self):
        request = PerevalPostRequest(
            beauty_title='Test Beauty Title',
            title='Test Title',
            user=UserModel(
                email='test@test.com',
                name='Test',
                fam='User',
                otc='Testovich',
                phone='+123456789'
            ),
            coords=CoordsModel(
                latitude=55.7522,
                longitude=37.6156,
                height=0
            ),
            level=LevelModel(
                winter=1,
                summer=2,
                autumn=3,
                spring=4
            ),
            images=[ImagesModel(data=b'123', name='test1.jpg'), ImagesModel(data=b'456', name='test2.jpg')]
        )
        response = await submit_data(request)
        assert response.status == 200
        assert response.message == 'Отправлено успешно'
        assert response.id is not None

    #  Tests that submitting data with an invalid user email returns a 500 error response
    @pytest.mark.asyncio
    async def test_invalid_user_email(self):
        request = PerevalPostRequest(
            beauty_title='Test Beauty Title',
            title='Test Title',
            user=UserModel(
                email='invalid_email',
                name='Test',
                fam='User',
                otc='Testovich',
                phone='+123456789'
            ),
            coords=CoordsModel(
                latitude=55.7522,
                longitude=37.6156,
                height=0
            ),
            level=LevelModel(
                winter=1,
                summer=2,
                autumn=3,
                spring=4
            ),
            images=[ImagesModel(data=b'123', name='test.jpg')]
        )
        response = await submit_data(request)
        assert response.status == 500
        assert response.message is not None

    #  Tests that submitting data with invalid coords returns a 500 error response
    @pytest.mark.asyncio
    async def test_invalid_coords(self):
        request = PerevalPostRequest(
            beauty_title='Test Beauty Title',
            title='Test Title',
            user=UserModel(
                email='test@test.com',
                name='Test',
                fam='User',
                otc='Testovich',
                phone='+123456789'
            ),
            coords=CoordsModel(
                latitude=91,
                longitude=181,
                height=0
            ),
            level=LevelModel(
                winter=1,
                summer=2,
                autumn=3,
                spring=4
            ),
            images=[ImagesModel(data=b'123', name='test.jpg')]
        )
        response = await submit_data(request)
        assert response.status == 500
        assert response.message is not None

    #  Tests that submitting data with invalid image data returns a 500 error response
    @pytest.mark.asyncio
    async def test_invalid_image_data(self):
        request = PerevalPostRequest(
            beauty_title='Test Beauty Title',
            title='Test Title',
            user=UserModel(
                email='test@test.com',
                name='Test',
                fam='User',
                otc='Testovich',
                phone='+123456789'
            ),
            coords=CoordsModel(
                latitude=55.7522,
                longitude=37.6156,
                height=0
            ),
            level=LevelModel(
                winter=1,
                summer=2,
                autumn=3,
                spring=4
            ),
            images=[ImagesModel(data=None, name='test.jpg')]
        )
        response = await submit_data(request)
        assert response.status == 500
        assert response.message is not None
