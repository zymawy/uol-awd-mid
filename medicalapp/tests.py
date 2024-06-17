from hypothesis.extra.django import TransactionTestCase as HypothesisTestCase
from django.test import Client
from rest_framework import status
from .models import MedicalRecord, Synonym, Concept, TreeNumber, \
	PharmacologicalAction, AllowableQualifier
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class MedicalRecordTests(HypothesisTestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser',
											 password='12345')
		self.client.login(username='testuser', password='12345')

		self.record = MedicalRecord.objects.create(
			mesh_id='D000006',
			term='Test Term',
			definition='Test Definition',
			entry_date=timezone.now()
		)

		self.medical_record_data = {
			"mesh_id": "D000001",
			"term": "Test Term",
			"definition": "Test Definition",
			"entry_date": "1999-01-01T00:00:00",
			"date_revised": "2023-02-26T00:00:00",
			"synonyms": [
				{"synonym": "Synonym1"},
				{"synonym": "Synonym2"}
			],
			"concepts": [
				{"concept_ui": "M0000001", "concept_name": "Calcimycin"}
			],
			"tree_numbers": [
				{"tree_number": "D02.355.291.933.125"}
			],
			"pharmacological_actions": [
				{"action_name": "Anti-Bacterial Agents"}
			],
			"allowable_qualifiers": [
				{"qualifier_name": "administration & dosage"}
			]
		}
		self.medical_record = MedicalRecord.objects.create(
			mesh_id="D000001",
			term="Test Term",
			definition="Test Definition",
			entry_date="1999-01-01T00:00:00",
			date_revised="2023-02-26T00:00:00",
		)
		Synonym.objects.create(medical_record=self.medical_record,
							   synonym="Synonym1")
		Synonym.objects.create(medical_record=self.medical_record,
							   synonym="Synonym2")
		Concept.objects.create(medical_record=self.medical_record,
							   concept_ui="M0000001", concept_name="Calcimycin")
		TreeNumber.objects.create(medical_record=self.medical_record,
								  tree_number="D02.355.291.933.125")
		PharmacologicalAction.objects.create(medical_record=self.medical_record,
											 action_name="Anti-Bacterial Agents")
		AllowableQualifier.objects.create(medical_record=self.medical_record,
										  qualifier_name="administration & dosage")

	def tearDown(self):
		MedicalRecord.objects.all().delete()
		Synonym.objects.all().delete()
		User.objects.all().delete()

	def test_create_medical_record(self):
		new_record_data = self.medical_record_data.copy()
		new_record_data['mesh_id'] = 'D000010'

		response = self.client.post(reverse('medicalrecord-list'),
									new_record_data, format='json')
		# print(response.content)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_it_will_fail_if_no_mech_id_exist(self):
		new_record_data = self.medical_record_data.copy()
		del new_record_data['mesh_id']

		response = self.client.post(reverse('medicalrecord-list'),
									new_record_data, format='json')
		# print(response.content)
		self.assertEqual(response.status_code,
						 status.HTTP_422_UNPROCESSABLE_ENTITY)

	def test_update_medical_record(self):
		updated_data = self.medical_record_data.copy()
		updated_data['term'] = 'Updated Term'
		response = self.client.put(
			reverse('medicalrecord-detail', args=[self.medical_record.id]),
			updated_data, content_type="application/json", format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['term'], 'Updated Term')

	def test_it_will_fail_when_no_record_for_update(self):
		updated_data = self.medical_record_data.copy()

		response = self.client.put(
			reverse('medicalrecord-detail', args=['0000']),
			updated_data, content_type="application/json", format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_medical_record(self):
		response = self.client.get(
			reverse('medicalrecord-detail', args=[self.medical_record.id]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['term'], 'Test Term')
		self.assertEqual(len(response.data['synonyms']), 2)
		self.assertEqual(response.data['synonyms'][0]['synonym'], 'Synonym1')

	def test_filter_records_by_term(self):
		response = self.client.get('/api/medicalrecords/?term=Test Term')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, 'Test Term')

	def test_delete_record(self):
		response = self.client.delete(f'/api/medicalrecords/{self.record.id}/',
									  format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		with self.assertRaises(MedicalRecord.DoesNotExist):
			MedicalRecord.objects.get(mesh_id='D000006')

	def test_filter_records_by_term(self):
		response = self.client.get('/api/medicalrecords/?term=Test Term')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, 'Test Term')

	def test_count_records(self):
		response = self.client.get('/api/medicalrecords/count/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('count', response.data)

	def test_complex_query(self):
		response = self.client.get('/api/medicalrecords/complex/?term_contains=Term&definition_contains=Test Definition')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, 'Test Definition')
		response = self.client.get('/api/medicalrecords/complex/?date_after=2023-01-01')
		print(response.json())  # Print the response content for debugging
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, 'Test Term')
		# self.assertContains(response, 'Another Term')
		self.assertNotContains(response, 'Different Term')
