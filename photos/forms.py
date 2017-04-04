from django import forms
from photos.models import Photo


class PhotoForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the name of this image.",
                           )

    source = forms.ImageField()

    class Meta:
        model = Photo
        fields = ('name', 'source', 'tag')
