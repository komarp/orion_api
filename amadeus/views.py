from django.shortcuts import render
from django.views.generic import FormView
from .forms import RequestForm
from .utils import APIFetcher
import orion.settings as settings

# Create your views here.


class PatientSearchView(FormView):
    form_class = RequestForm
    template_name = 'amadeus/search_patient.html'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + settings.ACCESS_TOKEN
    }

    def form_valid(self, form):
        response = APIFetcher(
            settings.API_URL,
            headers=self.headers).\
            get_response(form)
        if response.status_code == 200:
            content = response.json()
            if not content['total']:
                result = render(self.request, 'amadeus/callback_page.html')
            else:
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
                result = render(self.request, 'amadeus/patient_info.html', {'patient': patient_info_dict})
        else:
            result = render(self.request, 'amadeus/unsuccessful_page.html')
        return result
