from django.db import models
from django.contrib.auth.models import User
import os
import hashlib


class File(models.Model):
    # Opciones de visibilidad
    PUBLIC = "public"
    PRIVATE = "private"
    SHARED = "shared"

    VISIBILITY_CHOICES = [(PUBLIC, "Public"), (PRIVATE, "Private"), (SHARED, "Shared")]

    # Campos del modelo
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    size = models.IntegerField()
    date = models.DateTimeField()
    directory = models.CharField(max_length=255)
    hash = models.CharField(max_length=64, blank=True, null=True)  # Hash SHA-256
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="files_owned"
    )
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC
    )

    def __str__(self):
        return f"{self.name}"

    def calculate_hash(self):
        """
        Calcula el hash SHA-256 del archivo.
        """
        sha256 = hashlib.sha256()
        with open(self.path, "rb") as file:
            while True:
                data = file.read(65536)  # Lee en bloques de 64 KB
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()

    @classmethod
    def create_from_path(cls, file_path, user, visibility=PUBLIC):
        """
        Crea una instancia de File a partir de una ruta de archivo.
        """
        file_stats = os.stat(file_path)
        name = os.path.basename(file_path)
        directory = os.path.dirname(file_path)
        extension = os.path.splitext(file_path)[1]
        size = file_stats.st_size
        date = file_stats.st_mtime  # Usa la última modificación como fecha

        # Crear la instancia sin guardar aún
        file_instance = cls(
            name=name,
            path=file_path,
            extension=extension,
            size=size,
            date=date,
            directory=directory,
            owner=user,
            visibility=visibility,
        )

        # Calcular y asignar el hash
        file_instance.hash = file_instance.calculate_hash()

        return file_instance

    @classmethod
    def count_files_for_user(cls, user):
        """
        Cuenta cuántos archivos están relacionados con un usuario.
        """
        return cls.objects.filter(owner=user).count()


class FileAccess(models.Model):
    # Relación con el modelo File
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_level = models.CharField(
        max_length=10, choices=[("read", "Read"), ("write", "Write")], default="read"
    )

    def __str__(self):
        return f"Acceso de {self.user.username} a {self.file.name} ({self.permission_level})"


def user_can_access(file, user):
    """
    Verifica si un usuario tiene acceso a un archivo, dependiendo de su visibilidad o permisos.
    """
    # Si el archivo es público, cualquier usuario puede acceder
    if file.visibility == File.PUBLIC:
        return True

    # Si el archivo es privado, solo el propietario y los usuarios con acceso pueden verlo
    if file.visibility == File.PRIVATE:
        return (
            file.owner == user
            or FileAccess.objects.filter(file=file, user=user).exists()
        )

    # Si el archivo es compartido, verifica si el usuario tiene permiso
    if file.visibility == File.SHARED:
        return (
            file.owner == user
            or FileAccess.objects.filter(file=file, user=user).exists()
        )

    return False
