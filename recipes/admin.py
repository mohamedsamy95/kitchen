'''
Written by Samy <m.elsisi1995@gmail.com> on Wed 09.05.2023
Version 1.0
'''
from django.contrib import admin
from .models import Recipe

# Register your models here.
admin.site.register(Recipe)