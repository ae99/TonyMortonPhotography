from django.shortcuts import render

from photos.models import Tag, Photo

from photos.forms import PhotoForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import json

def index(request):
    tags_list = Tag.objects.all()
    photo_list = Photo.objects.all()[:20]
    photo_dict = [ obj.as_dict() for obj in photo_list ]
    print(photo_dict)
    photo_json = json.dumps(photo_dict)
    
    context_dict = {'tags': tags_list, 'photos': photo_list, 'json': photo_json}
    return render(request, 'photos/index.html', context=context_dict)


def about(request):
    return render(request, 'photos/about.html')

def show_photo(request, photo_name_slug):
    context_dict = {}

    try:
        photo = Photo.objects.get(slug=photo_name_slug)

        context_dict['photo'] = photo
    except Tag.DoesNotExist:
        context_dict['photo'] = None

    return render(request, 'photos/photo.html', context_dict)


def show_tag(request, tag_name_slug):
    context_dict = {}

    try:
        tag = Tag.objects.get(slug=tag_name_slug)

        photos = Photo.objects.filter(tag=tag)

        context_dict['photos'] = photos
        context_dict['tag'] = tag
    except Tag.DoesNotExist:
        context_dict['photos'] = None
        context_dict['tag'] = None

    return render(request, 'photos/tag.html', context_dict)

@login_required
def add_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return index(request)
        else:
            print(form.errors)
    else:
        form = PhotoForm()

    context_dict = {'form': form}
    return render(request, 'photos/addPhoto.html', context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django inbuilt user authentication
        user = authenticate(username=username, password=password)

        # Only runs if valid user
        if user:
            if user.is_active:  # User account not disabled
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account has been disabled")
        else:
            # Bad Login Details
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'photos/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))