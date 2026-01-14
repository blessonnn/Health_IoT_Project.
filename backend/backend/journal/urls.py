from django.urls import path
from .views import JournalEntryAPIView

urlpatterns = [
    path('journal/', JournalEntryAPIView.as_view(), name='journal-entry'),
]
