"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/users/register", views.register),
    path("api/v1/profile/add-credential", views.add_credential),
    path("api/v1/profile/share-create", views.share_create),
    path("api/v1/profile/get-share", views.get_share),
    path("api/v1/profile/emergency-access", views.emergency_access),
    path("api/v1/profile/emergency-access/grant", views.emergency_access_grant),
    path("api/v1/profile/privilege-rings", views.privilege_rings),
    path("api/v1/profile/update-info", views.update_info),
    path("api/v1/profile/revoke-access", views.revoke_access),
    path("api/v1/profile/share-create-link", views.share_create_link),
    path("api/v1/profile/public", views.public),
    path("api/v1/profile/export", views.export),
]
