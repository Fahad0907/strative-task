from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from unittest.mock import patch


class AverageTemperatureApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.api_url = '/api/avg-temperature'

    def test_average_temperature_api(self):
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.json())
        self.assertEqual(len(response.json()['data']), 10)


class TravelRecommendationApiTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.api_url = '/api/travel-recommendation'

        self.valid_params = {
            'friend_lat': 23.8103,
            'friend_lon': 90.4125,
            'dest_lat': 21.4272,
            'dest_lon': 92.0058,
            'travel_date': '2024-12-10',
        }

    @patch('requests.get')
    def test_travel_recommendation_api(self, mock_get):
        mock_friend_response = {
            "hourly": {
                "time": ["2024-12-10T14:00:00Z"],
                "temperature_2m": [30.5]
            }
        }

        mock_dest_response = {
            "hourly": {
                "time": ["2024-12-10T14:00:00Z"],
                "temperature_2m": [25.3]
            }
        }

        def side_effect(url, params):
            if params['latitude'] == self.valid_params['friend_lat']:
                return MockResponse(mock_friend_response, status.HTTP_200_OK)
            elif params['latitude'] == self.valid_params['dest_lat']:
                return MockResponse(mock_dest_response, status.HTTP_200_OK)
            return MockResponse({}, status.HTTP_400_BAD_REQUEST)

        mock_get.side_effect = side_effect

        response = self.client.get(self.api_url, self.valid_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "You should travel to your destination, it's cooler there!")

    def test_missing_parameters(self):
        response = self.client.get(self.api_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "Missing required parameters")


class MockResponse:
    """
    Mocked Response object to simulate requests.get responses.
    """
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data