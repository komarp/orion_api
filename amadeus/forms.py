from django import forms


class RequestForm(forms.Form):
    GENDER_CHOICES = [('male', 'Male'),
                      ('female', 'Female')]
    surname = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Surname'
        }))
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
        )
