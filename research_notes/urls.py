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
    path('', views.homepage, name='home'),
    path('admin/', admin.site.urls),
    path('me/login/', views.login_view, name="login"),
    path('me/logout/', views.logout_user, name="logout"),
    path('search-notes/', views.search_results, name="search"),
    path('tags', views.all_tags, name='all_tags'),
    path('tags/<tag_name>', views.tag, name='tag'),
    path('status', views.all_statuses, name='all_statuses'),
    path('status/<status_name>', views.status, name='status'),
    path('run-external/seed-the-database', views.seed_the_database, name='database-seed'),
    path('<path:path_to_file>', views.resolveObject, name="show-content"),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
