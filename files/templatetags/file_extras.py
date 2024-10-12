from django import template

register = template.Library()

@register.filter
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

