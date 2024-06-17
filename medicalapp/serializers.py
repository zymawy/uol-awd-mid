# medicalapp/serializers.py

from rest_framework import serializers
from .models import MedicalRecord, Synonym, Concept, TreeNumber, \
	PharmacologicalAction, AllowableQualifier


class SynonymSerializer(serializers.ModelSerializer):
	class Meta:
		model = Synonym
		fields = ['id', 'synonym']


class ConceptSerializer(serializers.ModelSerializer):
	class Meta:
		model = Concept
		fields = ['id', 'concept_ui', 'concept_name']


class TreeNumberSerializer(serializers.ModelSerializer):
	class Meta:
		model = TreeNumber
		fields = ['id', 'tree_number']


class PharmacologicalActionSerializer(serializers.ModelSerializer):
	class Meta:
		model = PharmacologicalAction
		fields = ['id', 'action_name']


class AllowableQualifierSerializer(serializers.ModelSerializer):
	class Meta:
		model = AllowableQualifier
		fields = ['id', 'qualifier_name']


class MedicalRecordSerializer(serializers.ModelSerializer):
	synonyms = SynonymSerializer(many=True, required=False)
	concepts = ConceptSerializer(many=True, required=False)
	tree_numbers = TreeNumberSerializer(many=True, required=False)
	pharmacological_actions = PharmacologicalActionSerializer(many=True,
															  required=False)
	allowable_qualifiers = AllowableQualifierSerializer(many=True,
														required=False)

	class Meta:
		model = MedicalRecord
		fields = ['id', 'mesh_id', 'term', 'definition', 'entry_date',
				  'date_revised', 'synonyms', 'concepts',
				  'tree_numbers', 'pharmacological_actions',
				  'allowable_qualifiers']

	def create(self, validated_data):
		synonyms_data = validated_data.pop('synonyms', [])
		concepts_data = validated_data.pop('concepts', [])
		tree_numbers_data = validated_data.pop('tree_numbers', [])
		pharmacological_actions_data = validated_data.pop(
			'pharmacological_actions', [])
		allowable_qualifiers_data = validated_data.pop('allowable_qualifiers',
													   [])
		medical_record = MedicalRecord.objects.create(**validated_data)

		for synonym_data in synonyms_data:
			Synonym.objects.create(medical_record=medical_record,
								   **synonym_data)

		for concept_data in concepts_data:
			Concept.objects.create(medical_record=medical_record,
								   **concept_data)

		for tree_number_data in tree_numbers_data:
			TreeNumber.objects.create(medical_record=medical_record,
									  **tree_number_data)

		for action_data in pharmacological_actions_data:
			PharmacologicalAction.objects.create(medical_record=medical_record,
												 **action_data)

		for qualifier_data in allowable_qualifiers_data:
			AllowableQualifier.objects.create(medical_record=medical_record,
											  **qualifier_data)

		return medical_record

	def update(self, instance, validated_data):
		synonyms_data = validated_data.pop('synonyms', None)
		concepts_data = validated_data.pop('concepts', None)
		tree_numbers_data = validated_data.pop('tree_numbers', None)
		pharmacological_actions_data = validated_data.pop(
			'pharmacological_actions', None)
		allowable_qualifiers_data = validated_data.pop('allowable_qualifiers',
													   None)

		instance.mesh_id = validated_data.get('mesh_id', instance.mesh_id)
		instance.term = validated_data.get('term', instance.term)
		instance.definition = validated_data.get('definition',
												 instance.definition)
		instance.entry_date = validated_data.get('entry_date',
												 instance.entry_date)
		instance.date_revised = validated_data.get('date_revised',
												   instance.date_revised)
		instance.save()

		if synonyms_data is not None:
			instance.synonyms.all().delete()
			for synonym_data in synonyms_data:
				Synonym.objects.create(medical_record=instance, **synonym_data)

		if concepts_data is not None:
			instance.concepts.all().delete()
			for concept_data in concepts_data:
				Concept.objects.create(medical_record=instance, **concept_data)

		if tree_numbers_data is not None:
			instance.tree_numbers.all().delete()
			for tree_number_data in tree_numbers_data:
				TreeNumber.objects.create(medical_record=instance,
										  **tree_number_data)

		if pharmacological_actions_data is not None:
			instance.pharmacological_actions.all().delete()
			for action_data in pharmacological_actions_data:
				PharmacologicalAction.objects.create(medical_record=instance,
													 **action_data)

		if allowable_qualifiers_data is not None:
			instance.allowable_qualifiers.all().delete()
			for qualifier_data in allowable_qualifiers_data:
				AllowableQualifier.objects.create(medical_record=instance,
												  **qualifier_data)

		return instance


class MedicalRecordDetailSerializer(serializers.ModelSerializer):
	synonyms = SynonymSerializer(many=True, required=False)

	class Meta:
		model = MedicalRecord
		fields = ['id', 'mesh_id', 'term', 'definition', 'entry_date',
				  'date_revised', 'synonyms']
