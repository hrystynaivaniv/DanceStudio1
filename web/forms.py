from django import forms
from core.models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'surname', 'phone', 'email', 'subscription']
