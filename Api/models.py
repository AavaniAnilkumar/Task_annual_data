from django.db import models

class WellData(models.Model):
    api_well_number = models.CharField(max_length=20, unique=True)
    oil_production = models.FloatField()
    gas_production = models.FloatField()
    brine_production = models.FloatField()

    def __str__(self):
        return self.api_well_number
