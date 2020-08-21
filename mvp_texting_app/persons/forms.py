from django import forms

from mvp_texting_app.persons.models import Person

class PersonChangeForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['id', 'metadata']
