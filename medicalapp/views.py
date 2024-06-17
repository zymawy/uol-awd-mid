# medicalapp/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from .models import MedicalRecord, Synonym
from .serializers import MedicalRecordSerializer, MedicalRecordDetailSerializer, \
	SynonymSerializer
from django.http import JsonResponse
from django.views import View
from asgiref.sync import sync_to_async
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class MedicalRecordPagination(PageNumberPagination):
	page_size = 10


class MedicalRecordViewSet(viewsets.ModelViewSet):
	queryset = MedicalRecord.objects.all()
	serializer_class = MedicalRecordSerializer
	pagination_class = MedicalRecordPagination
	ordering_fields = ['id', 'entry_date']
	ordering = ['id']

	# permission_classes = [IsAdminOrReadOnly]

	def get_serializer_class(self):
		if self.action in ['list', 'retrieve']:
			detail = self.request.query_params.get('detail',
												   'false').lower() == 'true'
			if detail:
				return MedicalRecordDetailSerializer
			else:
				return MedicalRecordSerializer
		return MedicalRecordSerializer

	def get_queryset(self):
		queryset = MedicalRecord.objects.all().order_by('entry_date')
		term = self.request.query_params.get('term', None)
		mesh_id = self.request.query_params.get('mesh_id', None)
		date_revised = self.request.query_params.get('date_revised', None)
		if term:
			queryset = queryset.filter(term__icontains=term)
		if mesh_id:
			queryset = queryset.filter(mesh_id__iexact=mesh_id)
		if date_revised:
			queryset = queryset.filter(date_revised__icontains=date_revised)
		return queryset

	@swagger_auto_schema(
		manual_parameters=[
			openapi.Parameter('term', openapi.IN_QUERY,
							  description="Filter by term",
							  type=openapi.TYPE_STRING),
			openapi.Parameter('mesh_id', openapi.IN_QUERY,
							  description="Filter by mesh id",
							  type=openapi.TYPE_STRING),
			openapi.Parameter('date_revised', openapi.IN_QUERY,
							  description="Filter by date revised",
							  type=openapi.TYPE_STRING),
		]
	)
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)

	@action(detail=False, methods=['get'])
	def count(self, request):
		count = MedicalRecord.objects.count()
		return Response({'count': count})

	@action(detail=False, methods=['get'])
	def complex(self, request):
		term_contains = request.query_params.get('term_contains', '')
		definition_contains = request.query_params.get('definition_contains',
													   '')
		date_after = request.query_params.get('date_after', '')

		records = MedicalRecord.objects.all()

		if term_contains:
			records = records.filter(term__icontains=term_contains)

		if definition_contains:
			records = records.filter(definition__icontains=definition_contains)

		if date_after:
			try:
				date_after_parsed = datetime.strptime(date_after,
													  '%Y-%m-%d').date()
				records = records.filter(entry_date__gte=date_after_parsed)
			except ValueError:
				return Response(
					{'error': 'Invalid date format. Use YYYY-MM-DD.'},
					status=400)

		serializer = MedicalRecordSerializer(records, many=True)
		return Response(serializer.data)


class AsyncMedicalRecordView(View):
	async def get(self, request, *args, **kwargs):
		records = await sync_to_async(list)(
			MedicalRecord.objects.all().order_by('entry_date'))
		data = [record.as_dict() for record in records]
		return JsonResponse(data, safe=False)


class SynonymViewSet(viewsets.ModelViewSet):
	queryset = Synonym.objects.all().order_by('id')
	serializer_class = SynonymSerializer
