from django.db import models

class Medicament(models.Model):
    med_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return self.name
    
from django.db import models

class MedicamentSummary(models.Model):
    med = models.ManyToManyField('Medicament', on_delete=models.CASCADE)
    qty_lt_3m = models.IntegerField(default=0)
    qty_3_6m = models.IntegerField(default=0)
    qty_gt_6m = models.IntegerField(default=0)

    def __str__(self):
        return self.med.name
