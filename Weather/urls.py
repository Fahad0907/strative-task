from django.urls import path
from Weather import views as weather_views


urlpatterns = [
    path('avg-temperature', weather_views.AverageTemperatureApi.as_view(), name='avg_temperature')
]