from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

doctors_choices ={
    ('family_practice_physician','Family Practice Physician'),
    ('internal_medicine_physician','Internal Medicine Physician'),
    ('pediatrician','Pediatrician'),
    ('allergist_immunologist','Allergist/Immunologist'),
    ('dermatologist','Dermatologist'),
    ('infectious_disease_doctor','Infectious Disease Doctor'),
    ('ophthalmologist','Ophthalmologist'),
    ('obstetrician_gynecologist','Obstetrician/Gynecologist (OB/GYN)'),
    ('cardiologist','Cardiologist'),
    ('geriatrician','Geriatric Medicine Doctor (Geriatrician)'),
    ('dentist','Dental Doctor (Dentist)'),
}

gender_choices = {
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    }

volume_choices = {
    ('ml','MiliLitres'),
    ('g','Grams'),
    ('mg','Miligrams'),
}

state = {
    ("draft","Draft"),
    ("done","Done"),
}

drug_choices = {
    ("Tablet","Tablet"),
    ("Capsule","Capsule"),
    ("Syrup","Syrup"),
    ("Injection","Injection"),
    ("Cream","Cream"),
    ("Ointment","Ointment"),
    ("Gel","Gel"),
    ("Powder","Powder"),
    ("Drops","Drops"),
    ("Inhaler","Inhaler"),
    ("Lotion","Lotion"),
    ("Suppository","Suppository"),
    ("Suspension","Suspension"),
    ("Spray","Spray"),
    ("Lozenge","Lozenge"),
    ("Patch","Patch"),
    ("Chewable Tablet","Chewable Tablet"),
    ("Effervescent Tablet","Effervescent Tablet"),
    ("Nasal Spray","Nasal Spray"),
    ("Eye Drops","Eye Drops"),
}

class Patient(models.Model):
    
    name = models.CharField(verbose_name='Patient Name')
    gender = models.CharField(choices=gender_choices,verbose_name='Gender')
    phone = models.CharField(verbose_name='Phone')
    address = models.CharField(verbose_name='Address')
    street = models.CharField(verbose_name='Street')
    country = models.CharField(verbose_name='Country')
    photo = models.ImageField(upload_to='patient_profile')
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='UserID')
    
    
    
        
        
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(verbose_name='Doctor Name')
    gender = models.CharField(choices=gender_choices,verbose_name='Gender')
    phone = models.CharField(verbose_name='Phone',blank=True)
    address = models.CharField(verbose_name='Address',blank=True)
    street = models.CharField(verbose_name='Street',blank=True)
    country = models.CharField(verbose_name='Country',blank=True)
    photo = models.ImageField(upload_to='doctor_profile',blank=True)
    doctor_type = models.CharField(choices=doctors_choices,verbose_name='Type')
    
    def __str__(self):
        return self.name
    
    
class Pharmacy(models.Model):
    name = models.CharField(verbose_name='Pharmacy Name')
    phone = models.CharField(verbose_name='Phone')
    address = models.CharField(verbose_name='Address')
    street = models.CharField(verbose_name='Street')
    country = models.CharField(verbose_name='Country')
    
    def __str__(self):
        return self.name
    
class Employee(models.Model):

    name = models.CharField(verbose_name='Employee Name')
    gender = models.CharField(choices=gender_choices,verbose_name='Gender')
    phone = models.CharField(verbose_name='Phone')
    address = models.CharField(verbose_name='Address')
    street = models.CharField(verbose_name='Street')
    country = models.CharField(verbose_name='Country')
    photo = models.ImageField(upload_to='employee_profile')
    pharmacy_id = models.ForeignKey(Pharmacy,on_delete=models.CASCADE,name="Pharmacy")
    
    
    def __str__(self):
        return self.name
    
    
    
class DrugManufacturer(models.Model):
    name = models.CharField(verbose_name='Manufacturer Name')
    phone = models.CharField(verbose_name='Phone',blank=True)
    contant_person = models.CharField(name = 'Contact person',blank=True)
    address = models.CharField(verbose_name='Address',blank=True)
    street = models.CharField(verbose_name='Street')
    country = models.CharField(verbose_name='Country') 
    def __str__(self):
        return self.name


class Flavours(models.Model):
    name = models.CharField(verbose_name='Name')
    
    def __str__(self):
        return self.name
    
     
class Drug(models.Model):
    name = models.CharField(verbose_name='Drug Name')
    image = models.ImageField(upload_to='drug_profile/')
    price = models.FloatField(verbose_name='Price')
    description = models.TextField(max_length=1000,verbose_name='Description',blank=True)
    manufacturer = models.ManyToManyField(DrugManufacturer,verbose_name='Manufacturer')
    condition_treated = models.CharField(max_length=100,verbose_name='Condition Treated',blank=True)
    flavour_id =  models.ManyToManyField(Flavours,verbose_name='Flavours')
    previous_price = models.FloatField(verbose_name='Previous price',blank=True)
    
    drug_type = models.CharField(choices=drug_choices,verbose_name='Type',default="Tablet")
    drug_url = models.CharField(verbose_name="Image url",blank=True)
    
    def _compute_drug_image_url(self, host):
        if self.image:
            print(f'this is url{self.image.name}')
            return f"{host}{self.image.name}"
        return None

    def save(self, *args, **kwargs):
        host = "http://127.0.0.1:8000/Pharmacy/media/"
        # Replace with your actual website URL
        
        self.drug_url = self._compute_drug_image_url(host)
        super().save(*args, **kwargs)

        

    
    
    
    def __str__(self):
        return self.name
    
class Prescription(models.Model):
        
    name = models.CharField(verbose_name='Prescription')
    doctor_id = models.ForeignKey(Doctor,verbose_name='Doctor',on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Patient")
    

    # Prescription details
    diagnosis = models.TextField(verbose_name="Diagnosis",default="Only attended to by the doctor")
    dosage = models.CharField(max_length=50, verbose_name="Dosage",default="Given with each drug")
    instructions = models.TextField(verbose_name="Instructions",default="Adhere to instructions")
    state = models.CharField(verbose_name="State",choices=state,default="draft")

    # Date and time
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Prescription Date")

    def __str__(self):
        return f"Prescription for {self.patient_id.name} by Dr. {self.doctor_id.name}"
    
    @property
    def computed_field(self):
        return f'PRES{self.id:04d}'
    
class prescriptionDrugs(models.Model):
    drug_id = models.ForeignKey(Drug, verbose_name='Drug Name', on_delete=models.CASCADE)   
    prescription_id = models.ForeignKey(Prescription,verbose_name='Prescription', on_delete=models.CASCADE) 
    dosage=models.TextField(verbose_name="Dosage",default="5 mg",null=True)
    quantity = models.FloatField(verbose_name="Quantity")
    flavors=models.ForeignKey(Flavours,verbose_name='Flavour',on_delete=models.CASCADE)
    drug_type = models.CharField(verbose_name="Medicine type",name="drug_type")
   
    def add_drugs(self,drugids:list,presid,flavours:list,quantity:list,dosage:list,drug_type:list):
        values=[]
        
        for ids in range(0,len(drugids)):
            drug_id = Drug.objects.get(id = drugids[ids])
            flavor = Flavours.objects.get(name=flavours[ids])
            
            values.append(prescriptionDrugs(drug_id=drug_id,prescription_id=presid,flavors=flavor,quantity=quantity[ids],dosage=dosage[ids],drug_type=drug_type[ids]))

        prescriptionDrugs.objects.bulk_create(values)


        
    
    
    
    
    