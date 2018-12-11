from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('suggest/', views.suggestion_view, name='suggestion'),
    path('review/', include('review.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, 
                        document_root=settings.STATIC_ROOT)
