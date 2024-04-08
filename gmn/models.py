import random
import uuid

from django.db import models


def generate_random_color():
    """Generate a random hex color code."""
    return f"#{random.randint(0, 0xFFFFFF):06x}"


class GMN(models.Model):
    """Groundwater Monitoring Network

    The abbreviation GMN was intentionally chosen, as it is the commonly used term in BRO land.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    data_owner = models.ForeignKey("api.Organisation", on_delete=models.CASCADE)
    bro_id = models.CharField(max_length=18)
    delivery_accountable_party = models.CharField(max_length=8, null=True)
    quality_regime = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=100, null=True)
    delivery_context = models.CharField(max_length=100, null=True)
    monitoring_purpose = models.CharField(max_length=100, null=True)
    groundwater_aspect = models.CharField(max_length=100, null=True)
    start_date_monitoring = models.DateField(null=True)
    object_registration_time = models.DateTimeField(null=True)
    registration_status = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=7, null=True, blank=True, default=None)

    def __str__(self):
        return self.bro_id

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = generate_random_color()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "GMN's"


class Measuringpoint(models.Model):
    """A measuringpoint is linked to a GMN.

    However, a measuring point is NOT a physical measuring point,
    but rather an abstraction of it. It is linked to a physical GMW monitoringtube,
    which can be replaced.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    data_owner = models.ForeignKey("api.Organisation", on_delete=models.CASCADE)
    gmn = models.ForeignKey(GMN, on_delete=models.CASCADE)
    measuringpoint_code = models.CharField(max_length=50, null=True)
    measuringpoint_start_date = models.DateField(null=True)
    gmw_bro_id = models.CharField(max_length=50, null=True)
    tube_number = models.CharField(max_length=50, null=True)
    tube_start_date = models.DateField(null=True)

    def __str__(self):
        return self.measuringpoint_code
