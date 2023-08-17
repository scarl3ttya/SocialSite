from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from . import forms, models


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = models.Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except models.Image.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})


@login_required
def image_create(request):
    if request.method == 'POST':
        form = forms.ImageCreateForm(data=request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully!')
            return redirect(new_image.get_absolute_url())
        else:
            messages.error(request, 'Error - form is not valid.')
    else:
        form = forms.ImageCreateForm(initial=request.GET.dict())

    return render(request, 'images/image/create.html',{'section': 'images', 'form': form})

def image_detail(request, id, slug):
    image = get_object_or_404(models.Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section':'images', 'image':image})