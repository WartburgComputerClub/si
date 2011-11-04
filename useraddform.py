from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class UserAddForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('first_name','last_name','username')
    def save(self,commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_active = True
        if commit:
            user.save()
        return user
    
