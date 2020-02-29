from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from . import models
from django.views.generic import ListView


# Create your views here.

from django.views.generic import ListView
from . import forms
# def all_materials(request):
#     material_list = models.Material.objects.all()
#     # material_list = models.Material.published.all()
#     return render(request,
#                   'material/list.html',
#                   {"materials": material_list})


class MaterialListView(ListView):
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

