from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import JournalEntry
from .serializers import JournalEntrySerializer


class JournalEntryAPIView(APIView):

    def get(self, request):
        entries = JournalEntry.objects.all().order_by('-created_at')
        serializer = JournalEntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = JournalEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Journal entry saved successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
