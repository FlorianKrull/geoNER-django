from django.contrib import admin
from .models import Collection, Document, Version, Entity, Gazetteer

# Register your models here.
myModels = [Collection, Document, Version, Entity, Gazetteer] 

admin.site.register(myModels)