from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def render_tree(context, tree):
    """Renderiza recursivamente un árbol de directorios."""

    html = "<ul class='file-tree'>"
    for key, value in tree.items():
        html += f"<li><span class='folder' onclick='toggleFiles(this)'>📁 {key}</span>"
        if isinstance(value, dict):  # Si es un diccionario (directorio)
            html += render_tree(context, value)  # Renderizar recursivamente
        elif isinstance(value, list):  # Si value es una lista de archivos
            for file_info in value:
                html += "<li>"
                html += f"<i class='fas {file_info['icon-class']}'></i>"
                html += f"<a href='{file_info['archivo']}'>{file_info['nombre']}.{file_info['extension']}</a>"
                html += f"<a href='#' onclick=\"viewFile('{file_info['archivo']}')\">👁️ Ver</a>"
                html += f"<a href='#' onclick=\"downloadFile('{file_info['archivo']}')\">⬇️ Descargar</a>"
                html += f"<a href='#' onclick=\"moveFile('{file_info['nombre']}')\">🔄 Mover</a>"
                html += f"<a href='#' onclick=\"deleteFile('{file_info['nombre']}')\">❌ Eliminar</a>"
                html += "</li>"
        html += "</li>"
    html += "</ul>"
    return mark_safe(html)
