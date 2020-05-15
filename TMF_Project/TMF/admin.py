from django.contrib import admin
from .models import *

myModels = [Author, Article, Quote, Comment]
admin.site.register(myModels)
