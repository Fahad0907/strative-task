from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
import requests
from concurrent.futures import ThreadPoolExecutor
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from lib.constant import STATUS, MESSAGE, DATA


cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


class AverageTemperatureApi(APIView):
    def get(self, request):
        location_url = 'https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json'
        weather_url = "https://api.open-meteo.com/v1/forecast"

        location_response = requests.get(location_url)
        if location_response.status_code != 200:
            return Response({
                MESSAGE: "Failed to fetch location data",
                DATA: {},
                STATUS: status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        
        location_data = location_response.json()['districts']
        district_avg_temperatures = []

        def fetch_weather(location):
            try:
                params = {
                    "latitude": location["lat"],
                    "longitude": location["long"],
                    "hourly": "temperature_2m",
                    "timezone": "auto",
                }
                response = openmeteo.weather_api(weather_url, params=params)[0]
                hourly = response.Hourly()
                hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

                hourly_data = {
                    "date": pd.date_range(
                        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                        freq=pd.Timedelta(seconds=hourly.Interval()),
                        inclusive="left"
                    )
                }
                hourly_data["temperature_2m"] = hourly_temperature_2m
                hourly_dataframe = pd.DataFrame(data=hourly_data)

                hourly_dataframe["hour"] = hourly_dataframe["date"].dt.hour
                filtered_data = hourly_dataframe[hourly_dataframe["hour"] == 14]
                two_pm_temps = filtered_data["temperature_2m"]
                
                avg_temp = two_pm_temps.mean()
                return {"district": location["name"], "average_temp_2pm": avg_temp}
            except Exception:
                return None

        with ThreadPoolExecutor() as executor:
            results = executor.map(fetch_weather, location_data)
            district_avg_temperatures = [result for result in results if result]

        sorted_districts = sorted(district_avg_temperatures, key=lambda x: x["average_temp_2pm"])
        top_10_coolest_districts = sorted_districts[:10]
        return Response({
            MESSAGE : "success",
            DATA: top_10_coolest_districts,
            STATUS: status.HTTP_200_OK
        },status=status.HTTP_200_OK)
    