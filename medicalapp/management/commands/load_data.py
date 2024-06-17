import xmltodict
from django.core.management.base import BaseCommand
from medicalapp.models import MedicalRecord, Synonym, Concept, TreeNumber, \
	PharmacologicalAction, AllowableQualifier
from datetime import datetime


class Command(BaseCommand):
	help = 'Load data from MeSH XML file into the database'

	def handle(self, *args, **kwargs):
		with open('medicalapp/desc2024_trimmed.xml', 'r', encoding='utf-8') as file:
			data = xmltodict.parse(file.read())
			records = data['DescriptorRecordSet']['DescriptorRecord']

			max_entries = 10000
			loaded_count = 0

			for record in records:
				if loaded_count >= max_entries:
					break

				mesh_id = record['DescriptorUI']
				term = record['DescriptorName']['String']
				definition = 'No definition available'
				synonyms = []
				entry_date = None
				date_revised = None

				if 'DateCreated' in record:
					date_created = record['DateCreated']
					year = date_created.get('Year', '1900')
					month = date_created.get('Month', '01')
					day = date_created.get('Day', '01')
					entry_date = datetime(int(year), int(month), int(day))

				if 'DateRevised' in record:
					date_revised_data = record['DateRevised']
					year = date_revised_data.get('Year', '1900')
					month = date_revised_data.get('Month', '01')
					day = date_revised_data.get('Day', '01')
					date_revised = datetime(int(year), int(month), int(day))

				if 'ConceptList' in record and 'Concept' in record[
					'ConceptList']:
					concept = record['ConceptList']['Concept']
					if isinstance(concept, list) and 'ScopeNote' in concept[0]:
						definition = concept[0]['ScopeNote']
					elif 'ScopeNote' in concept:
						definition = concept['ScopeNote']

					if isinstance(concept, list):
						for conc in concept:
							if 'TermList' in conc and 'Term' in conc[
								'TermList']:
								terms = conc['TermList']['Term']
								if isinstance(terms, list):
									for t in terms:
										synonyms.append(t['String'])
								else:
									synonyms.append(terms['String'])
					else:
						if 'TermList' in concept and 'Term' in concept[
							'TermList']:
							terms = concept['TermList']['Term']
							if isinstance(terms, list):
								for t in terms:
									synonyms.append(t['String'])
							else:
								synonyms.append(terms['String'])

				if not MedicalRecord.objects.filter(mesh_id=mesh_id).exists():
					# Create the MedicalRecord
					medical_record = MedicalRecord.objects.create(
						mesh_id=mesh_id,
						term=term,
						definition=definition,
						entry_date=entry_date,
						date_revised=date_revised,
					)
					# Create Synonyms
					for synonym in synonyms:
						Synonym.objects.create(medical_record=medical_record,
											   synonym=synonym)

					if 'ConceptList' in record and 'Concept' in record[
						'ConceptList']:
						concept_list = record['ConceptList']['Concept']
						if isinstance(concept_list, list):
							for concept in concept_list:
								Concept.objects.create(
									medical_record=medical_record,
									concept_ui=concept['ConceptUI'],
									concept_name=concept['ConceptName'][
										'String']
								)
						else:
							Concept.objects.create(
								medical_record=medical_record,
								concept_ui=concept_list['ConceptUI'],
								concept_name=concept_list['ConceptName'][
									'String']
							)

					# Extract and create TreeNumbers
					if 'TreeNumberList' in record and 'TreeNumber' in record[
						'TreeNumberList']:
						tree_numbers = record['TreeNumberList']['TreeNumber']
						if isinstance(tree_numbers, list):
							for tree_number in tree_numbers:
								TreeNumber.objects.create(
									medical_record=medical_record,
									tree_number=tree_number)
						else:
							TreeNumber.objects.create(
								medical_record=medical_record,
								tree_number=tree_numbers)

					# Extract and create PharmacologicalActions
					if 'PharmacologicalActionList' in record and 'PharmacologicalAction' in \
						record['PharmacologicalActionList']:
						actions = record['PharmacologicalActionList'][
							'PharmacologicalAction']
						if isinstance(actions, list):
							for action in actions:
								PharmacologicalAction.objects.create(
									medical_record=medical_record,
									action_name=action['DescriptorReferredTo'][
										'DescriptorName']['String']
								)
						else:
							PharmacologicalAction.objects.create(
								medical_record=medical_record,
								action_name=actions['DescriptorReferredTo'][
									'DescriptorName']['String']
							)

					# Extract and create AllowableQualifiers
					if 'AllowableQualifiersList' in record and 'AllowableQualifier' in \
						record['AllowableQualifiersList']:
						qualifiers = record['AllowableQualifiersList'][
							'AllowableQualifier']
						if isinstance(qualifiers, list):
							for qualifier in qualifiers:
								AllowableQualifier.objects.create(
									medical_record=medical_record,
									qualifier_name=
									qualifier['QualifierReferredTo'][
										'QualifierName']['String']
								)
						else:
							AllowableQualifier.objects.create(
								medical_record=medical_record,
								qualifier_name=
								qualifiers['QualifierReferredTo'][
									'QualifierName']['String']
							)

					loaded_count += 1

		self.stdout.write(
			self.style.SUCCESS(f'Done {loaded_count} records'))
