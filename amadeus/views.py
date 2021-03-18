from django.shortcuts import render
from django.views.generic import FormView
from .forms import RequestForm
import requests
import os
from django.template.response import TemplateResponse
# Create your views here.


class PatientSearchView(FormView):
    form_class = RequestForm
    template_name = 'amadeus/search_patient.html'

    def form_valid(self, form):
        KEY_URL = "https://api.orionhealth.io/fhir/3.0/Patient/"
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + os.getenv('ACCESS_TOKEN')
        }
        response = requests.get(KEY_URL, params={
            'gender': form.cleaned_data['gender'],
            'family': form.cleaned_data['surname']
        }, headers=headers)
        if response.status_code == 200:
            content = response.json()
            if not content['total']:
                return TemplateResponse(self.request, 'amadeus/callback_page.html')
            patient_info = content['entry'][0]['resource']
            patient_info_dict = {
                'first_name': patient_info['name'][0]['given'][0],
                'last_name': patient_info['name'][0]['family'],
                'gender': patient_info['gender'],
                'birth_date': patient_info['birthDate'],
                'country': patient_info['address'][0]['country'],
                'city': patient_info['address'][0]['city'],
                'street': patient_info['address'][0]['line'][0],
                'postal_code': patient_info['address'][0]['postalCode']
            }
            return render(self.request, 'amadeus/patient_info.html', {'patient': patient_info_dict})
        else:
            return TemplateResponse(self.request, 'amadeus/unsuccessful_page.html')

