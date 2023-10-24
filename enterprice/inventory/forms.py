from django import forms

class InputValueInventary(forms.Form):
    input = forms.CharField(label='', max_length=50, required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'Искать здесь....', 'required': False}))
