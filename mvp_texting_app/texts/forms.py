from django import forms

from mvp_texting_app.texts.models import TextDetails

class TextDetailsCreationForm(forms.ModelForm):

    class Meta:
        model = TextDetails
        fields = ['text_type', 'body']


class TextDetailsChangeForm(forms.ModelForm):

    class Meta:
        model = TextDetails
        fields = ['text_type', 'body']

