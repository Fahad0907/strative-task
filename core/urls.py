from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user-management/', include('Usermanagement.urls')),
    path('api/weather/', include('Weather.urls'))
]
