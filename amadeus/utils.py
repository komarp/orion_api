import requests


class APIFetcher:

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get_response(self, form):
        return requests.get(
            self.url,
            params={
                'gender': form.cleaned_data['gender'],
                'family': form.cleaned_data['surname']
            },
            headers=self.headers)
