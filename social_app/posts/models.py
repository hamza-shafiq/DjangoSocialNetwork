from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class HelpingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Posts(HelpingModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.user.name


class Country(HelpingModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Location(HelpingModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=50, null=True, blank=True)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)

    def __str__(self):
        return self.country.name

