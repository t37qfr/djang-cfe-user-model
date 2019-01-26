from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from django.db.models import Q

from .models import USERNAME_REGEX

from django.contrib.auth import get_user_model, authenticate
MyUser = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username / Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        #username and password valiation
        #user_qs1 = MyUser.objects.filter(username__iexact=username)
        #user_qs2 = MyUser.objects.filter(email__iexact=username)
        #user_qs_final = (user_qs1 | user_qs2).distinct()
        # Effective query, only one request
        user_qs_final = MyUser.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        ).distinct()

        if not user_qs_final.exists() and user_qs_final.count() != 1:
            raise forms.ValidationError('Invalid credentials...')

        the_user = authenticate(username=username, password=password)
        if not the_user:
            raise forms.ValidationError('Invalid Credentials!')
        '''user_obj = MyUser.objects.filter(username=username).first()
       if not user_obj:
            raise forms.ValidationError('Invalid Credentials!')
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError('Invalid Credentials!')'''

        #pass the data object to view
        self.cleaned_data['user_obj'] = the_user

        return super(UserLoginForm, self).clean(*args, **kwargs)

    '''def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        qs_exist = qs.exist()
        if not qs_exist and qs.count() != 1:
            raise forms.ValidationError('Invalid Credentials')
        return username'''

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username','email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username','email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]