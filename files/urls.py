from django.urls import path
from files.views import FileManagerView, home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", FileManagerView.as_view(), name="file_manager"),
]

