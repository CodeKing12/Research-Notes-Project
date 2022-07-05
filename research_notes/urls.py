"""research_notes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('<path:path_to_file>/', views.resolveObject, name="show-content"),
    path('tags', views.all_tags, name='all_tags'),
    path('tags/<tag_name>', views.tag, name='tag'),
    # path('<parent>/', views.displayFile, name="show-markdown-folder"),
    # path('<parent>/<file_name>/', views.displayFile, name="show-markdown-nosub"),
    # path('<parent>/<path:path_to_file>/<file_name>/', views.displayFile, name="show-markdown")
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
