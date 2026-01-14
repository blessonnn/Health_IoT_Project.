from django.urls import path
from .views import SensorDataAPIView

urlpatterns = [
    path('sensordata/', SensorDataAPIView.as_view(), name='sensor-data'),
]
