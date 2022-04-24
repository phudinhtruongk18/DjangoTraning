"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("controller.urls")),
    path('', include("user.urls")),

    # CATALOG AND PRODUCT HANDLE

    # healcheck
    path('healcheck/', include("healchecker.urls")),

    # OAuth
    path('', include('social_django.urls', namespace='social')),
    # auth wit api
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),

    path('', include("product.urls")),
    path('', include("catalog.urls")),
    path('', include("comment.urls")),
    path('', include("photo.urls")),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
