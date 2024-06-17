from django.contrib import admin

from django.contrib import admin
from .models import MedicalRecord, Synonym, Concept, TreeNumber, \
	PharmacologicalAction, AllowableQualifier


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
	list_display = (
	'mesh_id', 'term', 'definition', 'entry_date', 'date_revised',)
	search_fields = ('mesh_id', 'term', 'date_revised', 'entry_date')
	list_filter = ('entry_date', 'date_revised')


@admin.register(Synonym)
class SynonymAdmin(admin.ModelAdmin):
	list_display = ('medical_record', 'synonym')
	search_fields = ('medical_record__term', 'synonym')


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
	list_display = ('medical_record', 'concept_ui', 'concept_name')
	search_fields = ('medical_record__term', 'concept_name')


@admin.register(TreeNumber)
class TreeNumberAdmin(admin.ModelAdmin):
	list_display = ('medical_record', 'tree_number')
	search_fields = ('medical_record__term', 'tree_number')


@admin.register(PharmacologicalAction)
class PharmacologicalActionAdmin(admin.ModelAdmin):
	list_display = ('medical_record', 'action_name')
	search_fields = ('medical_record__term', 'action_name')


@admin.register(AllowableQualifier)
class AllowableQualifierAdmin(admin.ModelAdmin):
	list_display = ('medical_record', 'qualifier_name')
	search_fields = ('medical_record__term', 'qualifier_name')
