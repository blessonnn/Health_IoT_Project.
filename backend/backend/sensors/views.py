from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SensorData
from .serializers import SensorDataSerializer


class SensorDataAPIView(APIView):

    def get(self, request):
        data = SensorData.objects.all().order_by('-created_at')
        serializer = SensorDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sensor data saved successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
