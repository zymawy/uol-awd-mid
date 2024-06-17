# medicalapp/models.py

from django.db import models

class MedicalRecord(models.Model):
    mesh_id = models.CharField(max_length=50, unique=True)
    term = models.CharField(max_length=255)
    definition = models.TextField()
    entry_date = models.DateTimeField()
    date_revised = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.term


class Synonym(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='synonyms')
    synonym = models.CharField(max_length=255)

    def __str__(self):
        return self.synonym
class Concept(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, related_name='concepts', on_delete=models.CASCADE)
    concept_ui = models.CharField(max_length=100)
    concept_name = models.CharField(max_length=255)

class TreeNumber(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, related_name='tree_numbers', on_delete=models.CASCADE)
    tree_number = models.CharField(max_length=100)

class PharmacologicalAction(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, related_name='pharmacological_actions', on_delete=models.CASCADE)
    action_name = models.CharField(max_length=255)

class AllowableQualifier(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, related_name='allowable_qualifiers', on_delete=models.CASCADE)
    qualifier_name = models.CharField(max_length=255)
