from django.views import View
from django.shortcuts import render
from files.models import Archivo
from files.forms import ArchivoForm
from django.contrib import messages

class FileManagerView(View):

    def build_tree(self, files):
        """Construye un árbol de directorios a partir de la lista de archivos."""
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
            'epub': 'fa-book',
        }
        tree = {}
        for file in files:
            path_parts = (file.directorio or 'root').split('/')
            current_level = tree

            for part in path_parts:
                if part not in current_level:
                    current_level[part] = {}

                current_level = current_level[part]

            # Cambia esto para que los archivos se almacenen en una lista
            if 'archivos' not in current_level:
                current_level['archivos'] = []  # Lista para almacenar archivos

            # Agregar el archivo con su clase de ícono
            icon_class = icons.get(file.extension, 'fa-file')  # Obtener la clase del ícono
            current_level['archivos'].append({
                "nombre": file.nombre,
                "extension": file.extension,
                "archivo": file.archivo.url,
                "icon-class": icon_class,  # Agregar clase de ícono
            })

        return tree

    def get(self, request):
        files = Archivo.objects.all()
        return render(request, "file_manager.html", {"form": ArchivoForm(), "files_tree": self.build_tree(files)})


    def post(self, request):
        form = ArchivoForm(request.POST, request.FILES)
        files = Archivo.objects.all()
        if form.is_valid():
            form.save()
            messages.success(request, "Archivo creado correctamente")
            return render(request, "file_manager.html", {"form": ArchivoForm(), "files_tree": self.build_tree(files)})
        else:
            messages.error(request, f"Error al crear el archivo {form.errors}")
            return render(request, "file_manager.html", {"form": form, "files_tree": self.build_tree(files)})

def home(request):
    return render(request, "home.html")

