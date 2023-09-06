from django.contrib import admin

from .models import Doctor, Drug, DrugManufacturer,Patient,Pharmacy,Prescription,Flavours,Employee,prescriptionDrugs


class DoctorAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'gender',
        'phone',
        'address',
        'street',
        'country',
        'photo',
        'doctor_type',
    ]
    
class DrugAdmin(admin.ModelAdmin):
    fields = []
 
    
class DrugManufacturerAdmin(admin.ModelAdmin):
    fields = ['name','phone','contant_person','address','street','country',]
     
    
class PatientAdmin(admin.ModelAdmin):
    fields = ['name','gender','phone','address','street','country','photo']
    
class PharmacyAdmin(admin.ModelAdmin):
    fields = ['name','phone','address','street','country']
    
class PrescriptionAdmin(admin.ModelAdmin):
    fields = []
    
class FlavoursAdmin(admin.ModelAdmin):
    fields = []
class EmployeeAdmin(admin.ModelAdmin):
    fields = []



admin.site.register(Doctor)
admin.site.register(Drug)
admin.site.register(DrugManufacturer)
admin.site.register(Patient)
admin.site.register(Pharmacy)
admin.site.register(Prescription)
admin.site.register(Flavours)
admin.site.register(Employee)
admin.site.register(prescriptionDrugs)