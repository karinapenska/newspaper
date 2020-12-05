from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from bootstrap_datepicker_plus import DatePickerInput
#adds email field
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('dob','categories','image')


    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Favourites'
    )
    dob = forms.DateField( help_text="YYYY-MM-DD", label='Date of birth')
    def __init__(self, *args, **kwargs):
# first call parent's constructor
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
# there's a `fields` property now
        self.fields['image'].required = False
   # categories = forms.ModelMultipleChoiceField(
       # widget = forms.CheckboxSelectMultiple,
      #  queryset = Category.objects.all()
#    )
  #  dob= forms.DateField(label='What is your birth date?', widget=forms.SelectDateWidget)