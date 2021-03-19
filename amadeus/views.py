from django.shortcuts import render
from django.views.generic import FormView
from .forms import RequestForm
from .utils import OrionHealthAPI

# Create your views here.


class PatientSearchView(FormView):
    form_class = RequestForm
    template_name = 'amadeus/search_patient.html'

    def form_valid(self, form):
        gender = form.cleaned_data['gender']
        surname = form.cleaned_data['surname']
        patient = OrionHealthAPI().\
            get_patient(surname, gender)
        response_dct = {
            'success': render(self.request, 'amadeus/patient_info.html', {'patient': patient}),
            'undefined': render(self.request, 'amadeus/callback_page.html'),
            'unsuccessful': render(self.request, 'amadeus/unsuccessful_page.html')
        }
        return response_dct[patient['status']]
