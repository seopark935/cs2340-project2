from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Type your message...',
                'class': 'form-control rounded-pill',
                'autocomplete': 'off'
            }),
        }