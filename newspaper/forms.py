from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


from newspaper.models import Newspaper, Redactor, Topic


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control bg-gray-100 form-control-lg",
                       "placeholder": "Title..."}),
            "content": forms.Textarea(
                attrs={"class": "form-control bg-gray-100 form-control-lg",
                       "placeholder": "Content..."}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]
        widgets = {"name": forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "Enter topic name"})}


class RedactorCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control bg-gray-100 form-control-lg",
                   "placeholder": "First Name"}))
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control bg-gray-100 form-control-lg",
                   "placeholder": "Last Name"}
        ))
    years_of_experience = forms.IntegerField(
        min_value=0,
        max_value=100,
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control bg-gray-100 form-control-lg",
                   "placeholder": "Years of Experience"}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control bg-gray-100 form-control-lg",
            "placeholder": "Password"}))
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control bg-gray-100 form-control-lg",
            "placeholder": "Confirm Password"
        })
    )


    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "years_of_experience",
                  "password1",
                  "password2",)
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control bg-gray-100 form-control-lg",
                       "placeholder": "Username"}),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control bg-gray-100 form-control-lg",
                    "placeholder": "Email"}),
        }

    def save(self, commit=True):
        redactor = super(RedactorCreationForm, self).save(commit=False)
        redactor.first_name = self.cleaned_data["first_name"]
        redactor.last_name = self.cleaned_data["last_name"]
        redactor.years_of_experience = self.cleaned_data[
            "years_of_experience"]
        if commit:
            redactor.save()
        return redactor


    def clean_years_of_experience(self):
        return validate_years_of_experience(self.cleaned_data[
                                                "years_of_experience"])


class RedactorYearsOfExperienceUpdateForm(forms.ModelForm):
    years_of_experience = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control bg-gray-100 form-control-lg"}))

    class Meta:
        model = Redactor
        fields = ["years_of_experience"]

    def clean_years_of_experience(self):
        return validate_years_of_experience(self.cleaned_data[
                                                "years_of_experience"])


def validate_years_of_experience(years_of_experience):
    if years_of_experience < 0 or years_of_experience > 100:
        raise ValidationError(
            "Years of experience must be in the range from 0 to 100")
    return years_of_experience


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
        required=False,
    )


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
        required=False,
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
        required=False,
    )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())



class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "First Name",
                   "class": "form-control"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name",
                   "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    years_of_experience = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Years of experience",
                "class": "form-control",
                "min": 0,
                "max": 100,
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = Redactor
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "years_of_experience",
                  "password2")
