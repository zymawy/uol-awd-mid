# medicalapp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet, SynonymViewSet

router = DefaultRouter()
router.register(r'medicalrecords', MedicalRecordViewSet)
router.register(r'synonyms', SynonymViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
