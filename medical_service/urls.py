# medical_service/urls.py

from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin

schema_view = get_schema_view(
	openapi.Info(
		title="Medical API",
		default_version='v1',
		description="API documentation for the Medical service",
		terms_of_service="https://www.google.com/policies/terms/",
		contact=openapi.Contact(email="uol@medical.local"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include('medicalapp.urls')),
	path('', schema_view.with_ui('swagger', cache_timeout=0),
		 name='schema-swagger-ui'),

]
