from django.shortcuts import render, get_object_or_404, redirect

from photos.models import Category, Photo

from photos.forms import NewPhotoForm, EditPhotoForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    photos_all = Photo.objects.all()
    paginator = Paginator(photos_all, 2)
    page = request.GET.get('page', '1')

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    return render(request, 'photos/index.html', {'photos': photos})


def about(request):
    return render(request, 'photos/about.html')


def show_photo(request, photo_id):
    return render(request, 'photos/photo.html', {'photo': get_object_or_404(Photo, id=photo_id)})


@login_required
def newPhoto(request):
    if request.method == 'POST':
        form = NewPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('editPhoto') + "?id=" + form.instance.id)
    else:
        form = NewPhotoForm()
    return render(request, 'photos/newPhoto.html', {'form': form})

@login_required
def editPhoto(request):
    photo_id = request.GET.get('id', '')
    instance = get_object_or_404(Photo, id=photo_id)
    form = EditPhotoForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse('index'))
    return render(request, 'photos/editPhoto.html', {'photo': instance, 'form': form})


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