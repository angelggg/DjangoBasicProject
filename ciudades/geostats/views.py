from random import random

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN

from ciudades.geostats.models import UserEntity, UserStats, UserEntityImage


def login_view(request):
    args = {}
    if request.GET.get('no_user'):
        args['no_user'] = True
    return render(request, 'login.html', args)


def do_login_view(request):
    username = request.POST['uname']
    password = request.POST['pswd']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/login?no_user=true')


def sign_up_view(request):
    # Sign up view => redirect to home
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def create_entity_view(request):
    return render(request, 'create_entity.html')


@login_required
def user_entity_detail_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        user_entity = UserEntity.objects.get(pk=pk, user=request.user)
        entity = user_entity.entity
        ctype = user_entity.content_type.model
        images = user_entity.userentityimage_set.all()
        return render(request, 'entity_detail.html', {'entity': entity, 'type': ctype.capitalize(),
                                                      'user_entity_id': user_entity.pk, 'images': images})
    except ObjectDoesNotExist:
        return HttpResponseNotFound('Object not found, sorry')


def create_entities_view(request):
    from ciudades.geostats.content.handler import GeonamesHandler
    # Here we'll handle entities creation by asking to the remote api and returning results to user
    if not request.user.is_authenticated:
        code = HTTP_403_FORBIDDEN
        message = {'created': 0, 'error': 'LoginRequired'}
    else:
        user = request.user
        entity_id = request.POST.get('entity_id')
        try:
            message = {'created': GeonamesHandler().scrape_geonames(entity_id, user), 'error': False}
            code = HTTP_200_OK
        except AttributeError:
            message = {'created': 0, 'error': 'IdNotFound'}
            code = HTTP_400_BAD_REQUEST

    return JsonResponse(message, status=code)


@login_required
def user_home_view(request):
    towns = sorted(request.user.entities.get_towns(user=request.user)[:5], key=lambda x: random())
    regions = sorted(request.user.entities.get_regions(user=request.user)[:5], key=lambda x: random())
    countries = sorted(request.user.entities.get_countries(user=request.user)[:5], key=lambda x: random())
    return render(request, 'home.html', {'towns': towns, 'regions': regions, 'countries': countries})


@login_required
def entities_list_view(request, kind: str):
    towns, regions, countries = {}, {}, {}
    if kind == 'towns':
        towns = request.user.entities.get_towns(user=request.user).distinct()
    elif kind == 'regions':
        regions = request.user.entities.get_regions(user=request.user).distinct()
    elif kind == 'countries':
        countries = request.user.entities.get_countries(user=request.user).distinct()
    return render(request, 'home.html', {'towns': towns, 'regions': regions, 'countries': countries})


@login_required
def user_stats_view(request):
    # View
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'user-stats.html', {'user_stats': UserStats.objects.filter(user=request.user)})


@login_required
def upload_detail_image(request):
    redirect_url = request.META.get('HTTP_REFERER', '/')
    if request.FILES.get('image') and request.POST.get('user_entity_id'):
        image = request.FILES['image']
        uei = UserEntityImage(user_entity_id=request.POST.get('user_entity_id'))
        uei.image.save(image.name, image)
        uei.save()
    else:
        redirect_url = redirect_url.split('?')[0] + '?error=true'

    return redirect(redirect_url)
