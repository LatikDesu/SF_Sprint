import unittest
import pytest
from starlette.responses import JSONResponse

from app.models.schemas import PerevalResponseByEmail
from app.routers.submitdata import get_data_by_email


class TestGetDataByEmail(unittest.TestCase):
    #  Tests that the function returns a PerevalResponseByEmail object with a list of PerevalGetResponse objects for a valid email that has associated perevals
    @pytest.mark.asyncio
    async def test_valid_email_with_associated_perevals(self):
        response = await get_data_by_email('valid_email_with_associated_perevals@test.com')
        self.assertIsInstance(response, PerevalResponseByEmail)
        self.assertGreater(len(response.perevals), 0)

    #  Tests that the function returns a JSONResponse with status 204 and message 'Данные не найдены.' for a valid email that has no associated perevals
    @pytest.mark.asyncio
    async def test_valid_email_with_no_associated_perevals(self):
        response = await get_data_by_email('valid_email_with_no_associated_perevals@test.com')
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json(), {'status': 204, 'message': 'Данные не найдены.'})

    #  Tests that the function returns a JSONResponse with status 422 and message 'Неверный формат email' for an invalid email format
    @pytest.mark.asyncio
    async def test_invalid_email_format(self):
        response = await get_data_by_email('invalid_email_format')
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'status': 422, 'message': 'Неверный формат email'})

    #  Tests that the function returns a JSONResponse with status 204 and message 'Данные не найдены.' for a non-existent email
    @pytest.mark.asyncio
    async def test_non_existent_email(self):
        response = await get_data_by_email('non_existent_email@test.com')
        self.assertIsInstance(response, JSONResponse)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json(), {'status': 204, 'message': 'Данные не найдены.'})
