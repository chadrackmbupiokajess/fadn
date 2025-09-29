from django import forms
from django.core.exceptions import ValidationError
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)
        widgets = {
            'comment_body': forms.Textarea(attrs={'class':'form-control'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)  # Utiliser CharField pour validation personnalisée
    message = forms.CharField(widget=forms.Textarea)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise ValidationError('Le numéro de téléphone doit contenir uniquement des chiffres.')
        if len(phone) != 10:
            raise ValidationError('Le numéro de téléphone doit contenir exactement 10 chiffres.')
        return phone

from django import forms

class SearchForm(forms.Form):
    publication = forms.CharField(max_length=100, required=False, label='Recherche')
