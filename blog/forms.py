from django import forms

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login, 
    logout,
)

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            user=authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('this user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
            if not user.is_active:
                raise forms.ValidationError('This user is no longer active')
        return super(UserLoginForm,self).clean(*args,**kwargs)