from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from files.models import Archivo


class TestArchivos(TestCase):
    def setUp(self):
        # creando un archivo de prueba de 15 caracteres = 15 bytes
        self.image_file = ContentFile(b"fake_image_data", name="test_image.png")

        self.user = User.objects.create_user(
            username="test_user", password="124356789", email="test@test.com"
        )
        self.archivo = Archivo.objects.create(
            archivo=self.image_file,
            nombre="test_image",
            extension="png",
            size=100,
            fecha_creacion=timezone.now(),
            directorio="test",
        )

    def test_create_file(self):
        archivo = Archivo.objects.create(
            archivo=self.image_file,
            nombre="test_image_1",
            extension="png",
            size=100,
            fecha_creacion=timezone.now(),
            directorio="test",
        )
        self.assertEqual(archivo.nombre, "test_image_1")

    def test_size_file(self):
        self.assertEqual(self.archivo.size, 100)

    def test_size_format_byte(self):
        self.assertEqual(self.archivo.get_size_formatted(), "100 bytes")

    def test_size_format_KB(self):
        archivo = Archivo.objects.create(
            archivo=self.image_file,
            nombre="test_image",
            extension="png",
            size=1024,
            fecha_creacion=timezone.now(),
            directorio="test",
        )
        self.assertEqual(archivo.get_size_formatted(), "1.00 KB")

    def test_size_format_MB(self):
        archivo = Archivo.objects.create(
            archivo=self.image_file,
            nombre="test_image",
            extension="png",
            size=1048576,
            fecha_creacion=timezone.now(),
            directorio="test",
        )
        self.assertEqual(archivo.get_size_formatted(), "1.00 MB")

    def test_size_format_decimales(self):
        archivo = Archivo.objects.create(
            archivo=self.image_file,
            nombre="test_image",
            extension="png",
            size=43211243,
            fecha_creacion=timezone.now(),
            directorio="test",
        )
        self.assertEqual(archivo.get_size_formatted(), "41.21 MB")

    def test_create_simple_file_with_three_params(self):
        archivo = Archivo.objects.create(
            archivo=self.image_file, nombre="test_ddfimage_1", extension="png"
        )
        self.assertEqual(archivo.nombre, "test_ddfimage_1")

    def test_create_file_simple_with_one_param(self):
        archivo = Archivo.objects.create(archivo=self.image_file)
        self.assertEqual(archivo.nombre, "test_image")
        self.assertEqual(archivo.extension, "png")
        self.assertEqual(archivo.size, 15)

    def test_create_directory(self):
        archivo = Archivo.objects.create(
            archivo=self.image_file,
            nombre="test_image_1",
            extension="png",
            size=100,
            fecha_creacion=timezone.now(),
            directorio="test",
        )
        self.assertEqual(archivo.directorio, "test")

    def test_carpetas_for_files(self):
        archivo = Archivo.objects.create(
            archivo=self.image_file,
            nombre="test_image_1",
            extension="png",
            size=100,
            fecha_creacion=timezone.now(),
            directorio="test",
        )
        self.assertEqual(archivo.directorio, "test")

    def test_subcarpetas_for_files(self):
        archivo = Archivo.objects.create(
            archivo=self.image_file,
            nombre="test_image_1",
            extension="png",
            size=100,
            fecha_creacion=timezone.now(),
            directorio="test/test2/",
        )
        self.assertEqual(archivo.directorio, "test/test2/")
