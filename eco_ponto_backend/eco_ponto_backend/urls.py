from django.contrib import admin
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from django.urls import path, include

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls), 
    path('api/accounts/', include('accounts.urls')), 
    path('api/eco-points/', include('eco_points.urls')),
]
