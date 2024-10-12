import os
import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from django.conf import settings
from django.contrib.auth.models import User
from files.models import File


def scan_media_and_add_files(user):
    """
    Escanea la carpeta media, revisa si los archivos ya están en la base de datos
    y los agrega si no están.
    """
    media_dir = os.path.join(settings.BASE_DIR, "media")  # Ruta de la carpeta 'media'

    # 1. Verificar si hay archivos en la base de datos
    if File.objects.exists():
        print(
            "Archivos ya registrados en la base de datos. Escaneando media para detectar archivos nuevos..."
        )
    else:
        print(
            "No hay archivos en la base de datos. Se agregarán todos los archivos de media."
        )

    # 2. Recorrer los archivos en la carpeta 'media'
    for root, dirs, files in os.walk(media_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Verificar si el archivo ya está registrado (usando la ruta completa)
            if File.objects.filter(path=file_path).exists():
                print(f"Archivo '{file_name}' ya está registrado.")
                continue

            # 3. Crear el archivo si no existe en la base de datos
            file_instance = File.create_from_path(
                file_path, user, visibility=File.PUBLIC
            )

            # Asignar la fecha correctamente
            file_instance.date = make_aware(
                datetime.datetime.fromtimestamp(file_instance.date)
            )

            # Guardar el archivo en la base de datos
            file_instance.save()
            print(f"Archivo '{file_name}' agregado a la base de datos.")


class Command(BaseCommand):
    help = (
        "Escanea la carpeta media y registra archivos que no estén en la base de datos"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            type=str,
            help="El nombre de usuario que será el propietario de los archivos",
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]

        # Obtener el usuario
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"El usuario '{username}' no existe."))
            return

        # Escanear la carpeta media y agregar archivos no registrados
        scan_media_and_add_files(user)

        self.stdout.write(self.style.SUCCESS("Proceso completado."))
