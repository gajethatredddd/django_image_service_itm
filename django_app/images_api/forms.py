from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'path']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'path': forms.FileInput(attrs={'class': 'form-control'}),
        }
