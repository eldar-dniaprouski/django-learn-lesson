from django.shortcuts import render, get_object_or_404

from . import models


# Create your views here.


def all_materials(request):
    material_list = models.Material.objects.all()
    # material_list = models.Material.published.all()
    return render(request,
                  'material/list.html',
                  {"materials": material_list})


def material_details(request, year, month, day, slug):
    material = get_object_or_404(models.Material,
                                 slug=slug,
                                 status='public',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
    return render(request,
                  'material/detail.html',
                  {'material': material})
