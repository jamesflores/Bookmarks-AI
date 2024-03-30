from django import forms
from .models import Bookmark
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from crispy_forms.layout import Layout
from django_recaptcha.fields import ReCaptchaV2Checkbox
from django_recaptcha.fields import ReCaptchaField


def validate_url(url):
    # Check if URL does not start with http(s)://
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # Validate the URL
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError as e:
        # If URL is invalid, raise a validation error
        raise forms.ValidationError("Invalid URL")

    # Return the modified or original URL
    return url


class BookmarkAddForm(forms.ModelForm):
    url = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'})) 
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Bookmark
        fields = ['url', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'url',
            'note',
            Submit('submit', 'Save Bookmark'),
        )

    def clean_url(self):
        url = self.cleaned_data['url']
        return validate_url(url)


class BookmarkEditForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'category', 'description', 'notes' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = self.fields['category'].queryset.order_by('name')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'url',
            'title',
            'description',
            'notes',
            'category',
            Submit('submit', 'Save Bookmark'),
        )

    def clean_url(self):
        url = self.cleaned_data['url']
        return validate_url(url)