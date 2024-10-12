from django.views import View
from django.shortcuts import render
from files.models import Archivo
from files.forms import ArchivoForm
from django.contrib import messages


class FileManagerView(View):

    def get(self, request):
        files = Archivo.objects.all()
        # Crear un diccionario para agrupar por directorio
        files_by_directory = {}
        for file in files:
            directory = file.directorio or 'root'
            if directory not in files_by_directory:
                files_by_directory[directory] = []
            files_by_directory[directory].append(file)

        form = ArchivoForm()
        return render(request, "file_manager.html", {"form": form, "files_by_directory": files_by_directory})
    def post(self, request):
        form = ArchivoForm(request.POST,request.FILES)
        files = Archivo.objects.all()
        if form.is_valid():
            form.save()
            messages.success(request, "Archivo creado correctamente")
            return render(request, "file_manager.html",{"form":ArchivoForm(),"files":files})
        else:
            messages.error(request, f"Error al crear el archivo {form.errors}")
            return render(request, "file_manager.html", {"form": form, "files": files})


def home(request):
    return render(request, "home.html")

def get_file_icon(extension):
    icons = {
        'pdf': 'fa-file-pdf',
        'jpg': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'png': 'fa-file-image',
        'gif': 'fa-file-image',
        'txt': 'fa-file-alt',
        'doc': 'fa-file-word',
        'docx': 'fa-file-word',
        'xls': 'fa-file-excel',
        'xlsx': 'fa-file-excel',
        'zip': 'fa-file-archive',
        'rar': 'fa-file-archive',
        # Agrega más extensiones según lo necesario
    }
    return icons.get(extension, 'fa-file')
