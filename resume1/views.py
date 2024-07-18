from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from.forms import resume_form, RegistrationForm
from.forms import ResumeList
from.models import profile
from django.shortcuts import HttpResponse
import pdfkit
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, logout

@login_required
def index(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        about = request.POST.get('about')
        collage = request.POST.get('collage')
        degree = request.POST.get('degree')
        project1 = request.POST.get('project1')

        pr1 = profile(
            name = name,
            email = email,
            about = about,
            collage = collage,
            degree = degree,
            project1 = project1,
        )

        pr1.save()
        return HttpResponse("Successful!!")
    context = {
        "form": resume_form()
    }
    return render(request, "resume.html", context)

@login_required
def view_resume(request, id):
    pr_detailes = profile.objects.get(id=id)
    context = {
        "id": pr_detailes.id,
        "name" : pr_detailes.name,
        "email" : pr_detailes.email,
        "about": pr_detailes.about,
        "collage": pr_detailes.collage,
        "degree": pr_detailes.degree,
        "project1": pr_detailes.project1,
    }
    return render(request, "resume_detailes.html", context)


@login_required
def download(request, id):
    pr_detailes = profile.objects.get(id=id)
    context = {
        "id": pr_detailes.id,
        "name": pr_detailes.name,
        "email": pr_detailes.email,
        "about" : pr_detailes.about,
        "collage" : pr_detailes.collage,
        "degree": pr_detailes.degree,
        "project1":pr_detailes.project1,

    }

    template = loader.get_template('resume_detailes.html')
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }

    pdf = pdfkit.from_string(html,False,options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Context-Disposition'] = 'attachment'
    return response

    #return HttpResponse("Download successful!!")
def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

        return HttpResponse("Invalid data")

    form = RegistrationForm()
    return render(request, "register.html", {"form": form})

def userlogin(request):

    if request.method == "POST" :

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            form = login(request, user=user)
            messages.success(request, 'Login Successful!')
            return redirect('index')
        else:
            return HttpResponse("Invalid credentials")

    form = AuthenticationForm()
    return render(request, 'login.html',{'form': form})

@login_required
def userlogout(request):
    logout(request)
    return redirect('login')

@login_required
def resume_list(request):
    if request.method == "POST":
        print(request.__dict__)
        id = request.POST.get('resume_id')
        print(id)
        return view_resume(request, id=id)
    return render(request, 'resume-list.html', {"form" : ResumeList()})
