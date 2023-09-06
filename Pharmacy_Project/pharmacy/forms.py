from .models import Prescription
from django import forms


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['name', 'doctor_id','diagnosis','instructions', 'state','dosage']


    