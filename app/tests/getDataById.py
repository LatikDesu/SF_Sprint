import unittest
from unittest.mock import patch
import pytest
from sqlalchemy.exc import DatabaseError, IntegrityError

from app.routers.submitdata import get_data


class TestGetData(unittest.TestCase):
    #  Tests that data is retrieved successfully for a valid pereval_id
    @pytest.mark.asyncio
    async def test_retrieve_data_successfully(self):
        response = await get_data(1)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertIn('id', response.json())
        self.assertIn('status', response.json())
        self.assertIn('beauty_title', response.json())
        self.assertIn('title', response.json())
        self.assertIn('add_time', response.json())
        self.assertIn('user', response.json())
        self.assertIn('coords', response.json())
        self.assertIn('level', response.json())
        self.assertIn('images', response.json())

    #  Tests that a JSONResponse with status 204 and message 'Данные не найдены.' is returned if pereval is not found
    @pytest.mark.asyncio
    async def test_return_not_found(self):
        response = await get_data(9999)
        self.assertEqual(response.status_code, 204)
        self.assertIsInstance(response.json(), dict)
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 204)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Данные не найдены.')

    #  Tests that a JSONResponse with status 500 and message 'Ошибка при получении данных' is returned if there is a DatabaseError or IntegrityError
    @pytest.mark.asyncio
    async def test_return_error_on_database_error(self):
        with patch('app.routes.get_data.database.fetch_one') as mock_fetch_one:
            mock_fetch_one.side_effect = DatabaseError()
            response = await get_data(1)
            self.assertEqual(response.status_code, 500)
            self.assertIsInstance(response.json(), dict)
            self.assertIn('status', response.json())
            self.assertEqual(response.json()['status'], 500)
            self.assertIn('message', response.json())
            self.assertEqual(response.json()['message'], 'Ошибка при получении данных')

        with patch('app.routes.get_data.database.fetch_one') as mock_fetch_one:
            mock_fetch_one.side_effect = IntegrityError()
            response = await get_data(1)
            self.assertEqual(response.status_code, 500)
            self.assertIsInstance(response.json(), dict)
            self.assertIn('status', response.json())
            self.assertEqual(response.json()['status'], 500)
            self.assertIn('message', response.json())
            self.assertEqual(response.json()['message'], 'Ошибка при получении данных')
