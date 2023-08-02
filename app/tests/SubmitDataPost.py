# Dependencies:
# pip install pytest-mock
import pytest

from app.db_connection import database
from app.models.models import users_table, coords_table, pereval_add_table, images_table
from app.models.schemas import PerevalPostRequest, UserModel, CoordsModel, LevelModel, ImagesModel
from app.routers.submitdata import submit_data


class TestSubmitData:
    #  Tests that valid input data is submitted successfully
    @pytest.mark.asyncio
    async def test_valid_input_data(self, mocker):
        request = PerevalPostRequest(
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
        mocker.patch('app.routers.submit_data.coords_table.insert', return_value=2)
        mocker.patch('app.routers.submit_data.users_table.select', return_value=None)
        mocker.patch('app.routers.submit_data.users_table.insert', return_value=3)
        mocker.patch('app.routers.submit_data.pereval_add_table.insert', return_value=4)
        result = await submit_data(request)
        assert result.status == 200
        assert result.message == 'Отправлено успешно'
        assert result.id == 4

    #  Tests that a user who already exists in the database can submit data successfully
    @pytest.mark.asyncio
    async def test_existing_user(self, mocker):
        request = PerevalPostRequest(
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
        mocker.patch('app.routers.submit_data.coords_table.insert', return_value=2)
        mocker.patch('app.routers.submit_data.users_table.select', return_value={'id': 1})
        mocker.patch('app.routers.submit_data.users_table.update', return_value=1)
        mocker.patch('app.routers.submit_data.pereval_add_table.insert', return_value=4)
        result = await submit_data(request)
        assert result.status == 200
        assert result.message == 'Отправлено успешно'
        assert result.id == 4

    #  Tests that a new user can submit data successfully
    @pytest.mark.asyncio
    async def test_new_user(self, mocker):
        request = PerevalPostRequest(
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
        mocker.patch('app.routers.submit_data.coords_table.insert', return_value=2)
        mocker.patch('app.routers.submit_data.users_table.select', return_value=None)
        mocker.patch('app.routers.submit_data.users_table.insert', return_value=1)
        mocker.patch('app.routers.submit_data.pereval_add_table.insert', return_value=4)
        result = await submit_data(request)
        assert result.status == 200
        assert result.message == 'Отправлено успешно'
        assert result.id == 4

    #  Tests that an error is raised when user email is missing
    @pytest.mark.asyncio
    async def test_missing_user_email(self, mocker):
        request = PerevalPostRequest(
            beauty_title='Test Beauty Title',
            title='Test Title',
            other_titles='Test Other Titles',
            connect='Test Connect',
            user=UserModel(
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
        with pytest.raises(ValueError):
            await submit_data(request)

    #  Tests that an error is raised when latitude value is invalid
    @pytest.mark.asyncio
    async def test_invalid_latitude(self, mocker):
        request = PerevalPostRequest(
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
                latitude=91.0,
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
        with pytest.raises(ValueError):
            await submit_data(request)

    #  Tests that an error is raised when user name is missing
    @pytest.mark.asyncio
    async def test_missing_user_name(self, mocker):
        request = PerevalPostRequest(
            beauty_title='Test Beauty Title',
            title='Test Title',
            other_titles='Test Other Titles',
            connect='Test Connect',
            user=UserModel(
                email='test@test.com',
                fam='Test Fam',
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
        with pytest.raises(ValueError):
            await submit_data(request)

    #  Tests that the function 'submit_data' behaves correctly when the user email is valid
    @pytest.mark.asyncio
    async def test_user_email_is_valid(self, mocker):
        # Arrange
        request = PerevalPostRequest(
            beauty_title='beauty_title',
            title='title',
            other_titles='other_titles',
            connect='connect',
            user=UserModel(
                email='test@example.com',
                fam='fam',
                name='name',
                otc='otc',
                phone='phone'
            ),
            coords=CoordsModel(
                latitude=1.0,
                longitude=2.0,
                height=3
            ),
            level=LevelModel(
                winter='winter',
                summer='summer',
                autumn='autumn',
                spring='spring'
            ),
            images=[ImagesModel(data='data', name='name')]
        )
        mocker.patch.object(database, 'fetch_one', return_value={'id': 1})
        mocker.patch.object(database, 'execute', side_effect=[1, 2, 3])
        # Act
        response = await submit_data(request)
        # Assert
        assert response.status == 200
        assert response.message == 'Отправлено успешно'
        assert response.id == 3
        database.fetch_one.assert_called_once_with(
            users_table.select().where(users_table.c.email == request.user.email))
        database.execute.assert_has_calls([
            mocker.call(users_table.update().where(users_table.c.email == request.user.email).values(
                first_name=request.user.name, last_name=request.user.fam, patronymic=request.user.otc,
                phone=request.user.phone)),
            mocker.call(
                coords_table.insert().values(latitude=request.coords.latitude, longitude=request.coords.longitude,
                                             height=request.coords.height)),
            mocker.call(pereval_add_table.insert().values(beauty_title=request.beauty_title, title=request.title,
                                                          other_titles=request.other_titles, connect=request.connect,
                                                          coords_id=2, user_id=1, level_winter=request.level.winter,
                                                          level_summer=request.level.summer,
                                                          level_autumn=request.level.autumn,
                                                          level_spring=request.level.spring)),
            mocker.call(images_table.insert().values(pereval=3, data='data', name='name'))
        ])
