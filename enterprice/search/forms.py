from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class InputValue(forms.Form):
    input = forms.CharField(label='', max_length=50,
                            widget=forms.TextInput(attrs={'placeholder': 'Искать здесь....'}))
