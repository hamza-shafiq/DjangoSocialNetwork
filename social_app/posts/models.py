from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class HelpingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name_plural = "helping_model"


class Posts(HelpingModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "posts"

    def __str__(self):
        return self.user.name


class PostLikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, blank=True, null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "post_like_dislike"


class HolidayInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    event = models.CharField(max_length=250, null=True, blank=True)
    week_day = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "holiday_information"

    @classmethod
    def create_event(cls, info):
        try:
            new_event, _created = cls.objects.get_or_create(**info)
            return new_event
        except Exception as e:
            print("Exception while creating new holiday info at sign-up. Error: {}".format(str(e)))
            return None


class Location(HelpingModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = "location"

    def __str__(self):
        return self.country

    @classmethod
    def create_user_location(cls, geo_location):
        try:
            new_location, _created = cls.objects.get_or_create(**geo_location)
            return new_location
        except Exception as e:
            print("Exception while creating user location. Error: {}".format(str(e)))
            return None
