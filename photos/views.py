from django.shortcuts import render, get_object_or_404, redirect

from photos.models import Category, Photo

from photos.forms import NewPhotoForm, EditPhotoForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def setup(request):
    photos = Photo.objects.filter(name='')
    return render(request, 'photos/setup.html', {'photos':photos})

def index(request, category=None):
    if category == None:
        photos_all = Photo.objects.all().order_by("-id")
    else:
        photos_all = Photo.objects.filter(category=category).order_by("id")
    paginator = Paginator(photos_all, 20)
    page = request.GET.get('page', '1')
    
    category_list = Category.objects.all()
    
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    
    showNav = paginator.num_pages >= 2
        
    
    return render(request, 'photos/index.html', {'photos': photos, 'category':category, 'categories':category_list, 'showNav': showNav})

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return index(request, category)

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
            return redirect(reverse('editPhoto') + "?id=" + str(form.instance.id))
    else:
        form = NewPhotoForm()
    return render(request, 'photos/newPhoto.html', {'form': form})

@login_required
def editPhoto(request):
    photo_id = request.GET.get('id', '')
    instance = get_object_or_404(Photo, id=photo_id)
    
    if request.method == 'POST':
        form = EditPhotoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = EditPhotoForm(instance=instance)

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