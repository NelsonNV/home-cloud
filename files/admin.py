from django.contrib import admin
from files.models import Archivo


@admin.register(Archivo)
class FileAdmin(admin.ModelAdmin):
    pass
