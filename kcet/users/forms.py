from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, PreviousDegree, KCETResult, PUResult, FormLastActive, DocumentVerified
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def year_choices():
    return [(r,r) for r in range(2018, datetime.date.today().year+1)]
    
def current_year():
    return datetime.date.today().year

class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
                  'full_name', 'ph_number',
                  'address',
                  'bc_number', 'dob'
                 ]

class PreviousDegreeForm(forms.ModelForm):
    # batch = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

    class Meta:
        model = PreviousDegree
        fields = ['college_id', 'usn']

class KCETResultForm(forms.ModelForm):
    rank = forms.IntegerField(validators=[MaxValueValidator(1400), MinValueValidator(1)])
    marks = forms.IntegerField(validators=[MaxValueValidator(180), MinValueValidator(0)])

    class Meta:
        model = KCETResult
        fields = ['rank', 'marks']

class PUResultForm(forms.ModelForm):
    marks = forms.IntegerField(validators=[MaxValueValidator(500), MinValueValidator(0)])
    year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

    class Meta:
        model = PUResult
        fields = ['pu_roll','marks', 'year']

class FormLastActiveForm(forms.ModelForm):
    class Meta:
        model = FormLastActive
        fields = '__all__'

class DocumentVerifiedForm(forms.ModelForm):
    class Meta:
        model = DocumentVerified
        fields = ['unique_id', 'verified']