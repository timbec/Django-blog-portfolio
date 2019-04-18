from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import ContactForm

# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['comment']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['comment']
            try:
                send_mail(subject, message, from_email,
                          ['timbeckett@ymail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "pages/contact.html", {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')
