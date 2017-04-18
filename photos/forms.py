# Import required files
from django import forms
from photos.models import Photo


class NewPhotoForm(forms.ModelForm):
    class Meta:
        # Defines form for model/class 'Photo'
        model = Photo
        # Allow input of the following fields
        fields = ('name', 'source')


class EditPhotoForm(forms.ModelForm):
    class Meta:
        # Defines form for model/class 'Photo'
        model = Photo
        # Exclude no fields, i.e. include all fields.
        exclude = ()
