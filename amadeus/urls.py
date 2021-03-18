from django.urls import path
from .views import PatientSearchView


app_name = 'amadeus'


urlpatterns = [
    path('', PatientSearchView.as_view(), name='patient-search'),
]
