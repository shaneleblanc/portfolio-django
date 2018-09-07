from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Your name',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Your email',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Your message',
                              max_length=5000,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
