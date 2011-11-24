
# Create your views here.
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.template import RequestContext
from si.forms import UserAddForm,SigninForm
from si.models import Session
from django.core.urlresolvers import reverse

def register_view(request):
    return HttpResponse("Hello!")

def index(request):
    return HttpResponseRedirect('admin/')
    if request.user.is_authenticated():
        return render_to_response('index.html')
    else:
        return HttpResponseRedirect(reverse('si.views.login_view'))

def register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        form = UserAddForm(data)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('../admin/')
    else:
        form = UserAddForm()
        
    return render_to_response("si/register.html", {
        'form' : form,
        'title': 'Registration'
    },context_instance=RequestContext(request))

def signin(request,session):
    flag = False
    sess = Session.objects.get(pk=session)
    form = SigninForm()

    if request.user.is_authenticated():
        if request.user == sess.user:
            flag = True
            #response.set_cookie('valid',True,max_age=120)
        logout(request)

    response = render_to_response("si/signin.html",{
            'form': form,
            'title': ('Signin ' + str(sess.date))
            },context_instance=RequestContext(request))
    print flag
    if (flag):
        response.set_cookie('valid',True,max_age=120)
        return response
    if request.COOKIES.get('valid'):
        return response
    else:
        return HttpResponse("COOKIE TIMED OUT!")
    print request.COOKIES.get('valid')
#return HttpResponse("Hello World!" + str(session))
