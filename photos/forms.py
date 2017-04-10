from django import forms
from photos.models import Photo


class NewPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('name', 'source')

class EditPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('id',)