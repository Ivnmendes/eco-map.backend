from django.urls import path
from .views import GeocodeView, ReverseGeocodeView

urlpatterns = [
    path("geocode/", GeocodeView.as_view(), name="geocode"),
    path("reverse-geocode/", ReverseGeocodeView.as_view(), name="reverse-geocode"),
]
