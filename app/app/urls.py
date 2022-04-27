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

from category.views import CategoryListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('me/', include("user.urls")),

    # CATALOG AND PRODUCT URL
    path('', CategoryListView.as_view(), name='category'),
    path('category/', include("category.urls")),
    path('product/', include("product.urls")),
    path('comment/', include("comment.urls")),

    # OAuth
    path('', include('social_django.urls', namespace='social')),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # auth wit api
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
# else (production case) will be handled by nginx
