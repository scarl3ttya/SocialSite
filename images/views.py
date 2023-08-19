from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage,  PageNotAnInteger
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
import redis
from django.conf import settings
from actions.utils import create_action
from . import forms, models


# connect to redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required
def image_list(request):
    images = models.Image.objects.all()
    paginator = Paginator(images, 4)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request, 'images/image/list_images.html',{'images':images})
    return render(request, 'images/image/list.html', {'images':images})


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
                create_action(request.user, 'likes', image)
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
            create_action(request.user, 'bookmarded image', new_image)
            messages.success(request, 'Image added successfully!')
            return redirect(new_image.get_absolute_url())
        else:
            messages.error(request, 'Error - form is not valid.')
    else:
        form = forms.ImageCreateForm(initial=request.GET.dict())

    return render(request, 'images/image/create.html',{'section': 'images', 'form': form})

def image_detail(request, id, slug):
    image = get_object_or_404(models.Image, id=id, slug=slug)
    total_views = r.incr(f'image:{image.id}:views')
    r.zincrby('image_ranking', 1, image.id)
    return render(request, 'images/image/detail.html', {'section':'images', 'image':image, 'total_views': total_views})


@login_required
def image_ranking(request):
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewed = list(models.Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'section': 'images', 'most_viewed': most_viewed})