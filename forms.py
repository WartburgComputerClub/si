from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from si.models import Session
from django import forms

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
    def clean_student(self):
        students = self.cleaned_data['student']
        course = self.cleaned_data['course']
        for s in students:
            if s.course != course:
                raise forms.ValidationError("Students must be part of selected course!")
        return self.cleaned_data['student']

class UserAddForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75) 
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')
    def save(self,commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_active = True
        user.is_staff = True
        if commit:
            user.save()
        leaders = Group.objects.get(name='leaders')
        leaders.user_set.add(user)
        leaders.save()
        return user
    
