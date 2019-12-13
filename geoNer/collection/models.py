from django.db import models
from django.contrib.auth.models import User
from django_google_maps import fields as map_fields

# Create your models here.

class Collection(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)


class Document(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey(Collection, related_name='document',on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='document',on_delete=models.CASCADE)


class Version(models.Model):
    text = models.TextField(max_length=10000)
    document = models.ForeignKey(Document, related_name='version',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='version',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

class Entity(models.Model):
    text = models.TextField(max_length=200)
    version = models.ForeignKey(Version, related_name='entity',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='entity',on_delete=models.CASCADE)
    geolocation = map_fields.GeoLocationField(max_length=100)

class Gazetteer(models.Model):
    location = models.TextField(max_length=500)
    loc_id = models.FloatField()
    lat = models.FloatField()
    lon = models.FloatField()
