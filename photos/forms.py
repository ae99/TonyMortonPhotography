# Import required files
from django import forms
from django.forms import modelformset_factory


from photos.models import Photo, Category


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
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={
            'placeholder': 'New Category',
        })
    )

    class Meta:
        model = Category
        fields = ('name',)


CategoryFormSet = modelformset_factory(Category, form=CategoryForm, can_delete=True)
