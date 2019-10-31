from django.db import models
from django.contrib.auth.models import User

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
    text = models.TextField(max_length=4000)
    document = models.ForeignKey(Document, related_name='version',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='version',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)