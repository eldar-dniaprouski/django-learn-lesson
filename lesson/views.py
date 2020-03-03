from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from . import models
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.generic import ListView
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required
# def all_materials(request):
#     material_list = models.Material.objects.all()
#     # material_list = models.Material.published.all()
#     return render(request,
#                   'material/list.html',
#                   {"materials": material_list})


class MaterialListView(LoginRequiredMixin, ListView):
    queryset = models.Material.objects.all()
    context_object_name = 'materials'
    template_name = 'material/list.html'


def material_details(request, year, month, day, slug):
    material = get_object_or_404(models.Material,
                                 slug=slug,
                                 # status='public',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
    return render(request,
                  'material/detail.html',
                  {'material': material})


def share_material(request, material_id):
    material = get_object_or_404(models.Material, id=material_id)
    sent = False

    if request.method == 'POST':
        form = forms.EmailMaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # prepare data for email
            material_uri = request.build_absolute_uri(
                    material.get_absolute_url(),
            )
            subj = "{} ({}) recommends {}".format(
                    cd['name'],
                    cd['my_email'],
                    material.title,
            )
            body = "{title} at {link} \n\n{person}'s comment: {comment}".format(
                    title=material.title,
                    link=material_uri,
                    person=cd['name'],
                    comment=cd['comment'],
            )
            send_mail(subj, body, 'admin@myletter.com', [cd['to'], ])
            sent = True
    else:
        form = forms.EmailMaterialForm()
    return render(request, 'material/share.html', {'material': material,
                                                    'form': form,
                                                    'sent': sent})


def create_form(request):
    if request.method == 'POST':
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            new_material.slug = new_material.title.replace(" ", "-")
            new_material.save()
            return render(request,
                          'material/detail.html',
                          {'material': new_material})
    else:
        material_form = forms.MaterialForm()
    return render(request, "material/create_material.html", {'form': material_form})


def user_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                    request,
                    username=cd['username'],
                    password=cd['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Auth success')
                else:
                    HttpResponse('Inactive user')
            else:
                return HttpResponse('invalid credentials')
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})
