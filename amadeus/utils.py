import requests
from django.conf import settings


class OrionHealthAPI:

    def __init__(self):
        self._url = settings.ACCESS_TOKEN
        self._headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {settings.ACCESS_TOKEN}'
        }

    def get_patient(self, surname, gender):
        response = requests.get(
            self._url,
            params={
                'gender': gender,
                'family': surname
            },
            headers=self._headers)
        if response.status_code == 200:
            content = response.json()
            if not content['total']:
                patient_info_dict = {
                    'status': 'undefined'
                }
            else:
                patient_info = content['entry'][0]['resource']
                patient_info_dict = {
                    'status': 'success',
                    'first_name': patient_info['name'][0]['given'][0],
                    'last_name': patient_info['name'][0]['family'],
                    'gender': patient_info['gender'],
                    'birth_date': patient_info['birthDate'],
                    'country': patient_info['address'][0]['country'],
                    'city': patient_info['address'][0]['city'],
                    'street': patient_info['address'][0]['line'][0],
                    'postal_code': patient_info['address'][0]['postalCode']
                }
        else:
            patient_info_dict = {'status': 'unsuccessful'}
        return patient_info_dict
