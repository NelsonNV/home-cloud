import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Archivo(models.Model):
    objects = models.Manager()
    PUBLIC = "public"
    PRIVATE = "private"
    SHARED = "shared"

    VISIBILITY_CHOICES = [(PUBLIC, "Public"), (PRIVATE, "Private"), (SHARED, "Shared")]

    archivo = models.FileField(upload_to="files/")
    nombre = models.CharField(max_length=255, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    directorio = models.CharField(max_length=255, blank=True, null=True)
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC
    )

    def __str__(self) -> str:
        return f"{self.nombre}.{self.extension} <{self.directorio}>"

    def full_name(self):
        return f"{self.nombre}.{self.extension}"

    def get_size_formatted(self):
        bite = 1024
        size = self.size

        if size < bite:
            return f"{size} bytes"
        elif size < bite * bite:
            return f"{size / bite:.2f} KB"
        elif size < bite * bite * bite:
            return f"{size / bite / bite:.2f} MB"
        elif size < bite * bite * bite * bite:
            return f"{size / bite / bite / bite:.2f} GB"

    def save(self, *args, **kwargs):
        if self.size is None:
            self.size = self.archivo.size
        if self.extension is None:
            self.extension = self.archivo.name.split(".")[-1]
        if self.nombre is None:
            self.nombre = self.archivo.name.split(".")[0]
        if self.visibility is None:
            self.visibility = self.PUBLIC
        if self.directorio:
            self.archivo.name = os.path.join(self.directorio, self.full_name())

        # Asegúrate de que el directorio existe
        full_directory = os.path.join(settings.MEDIA_ROOT, self.directorio or "")
        os.makedirs(full_directory, exist_ok=True)

        super().save(*args, **kwargs)


