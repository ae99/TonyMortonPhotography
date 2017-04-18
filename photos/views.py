from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from photos.models import Category, Photo

from photos.forms import NewPhotoForm, EditPhotoForm


# View for index
def index(request, category_slug="all", page_number=1):
    # If category is defined - see category view
    if category_slug == "all":
        photos_all = Photo.objects.all().order_by("-id")  # Return entire Database in reverse chronological order
        category = None
    else:
        category = get_object_or_404(Category, slug=category_slug)
        photos_all = Photo.objects.filter(category=category).order_by("id")  # Return Database for specific Category
    paginator = Paginator(photos_all, 20)  # Paginates all photos into pages of 20

    category_list = Category.objects.all()

    # Error trapping, set pages
    try:
        photos = paginator.page(page_number)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    # Only show page numbers if more than 1 pages.
    showNav = paginator.num_pages >= 2

    context = {
        'photos': photos,
        'category_slug': category_slug,  # Different from category - may be all
        'category': category,
        'categories': category_list,
        'showNav': showNav
    }

    # Send to index.html template with context of photos, category etc.
    return render(request, 'index.html', context)



def about(request):
    return render(request, 'about.html')


# Individual photo
def show_photo(request, photo_id):
    return render(request, 'photo.html', {'photo': get_object_or_404(Photo, id=photo_id)})


@login_required  # Require user to be logged in for this view.
def newPhoto(request):
    if request.method == 'POST':  # If HTTP Post Method
        form = NewPhotoForm(request.POST, request.FILES)  # Photo Form -> forms.py
        if form.is_valid():
            form.save()
            return redirect(reverse('editPhoto', args=(form.instance.id,)))  # Redirect to edit page
    else:
        form = NewPhotoForm()
    return render(request, 'newPhoto.html', {'form': form})


@login_required
def editPhoto(request, photo_id):
    # photo_id = request.GET.get('id', '')
    instance = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':
        form = EditPhotoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = EditPhotoForm(instance=instance)

    return render(request, 'editPhoto.html', {'photo': instance, 'form': form})


@login_required
def deletePhoto(request, photo_id):
    instance = get_object_or_404(Photo, id=photo_id)
    if request.POST.get('delete'):
        instance.delete()
        return redirect(reverse('index'))
    elif request.POST.get('cancel'):
        return redirect(reverse('editPhoto', args=(photo_id,)))
    return render(request, 'deletePhoto.html', {'photo': instance})



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
                return redirect(reverse('index'))
            else:
                return HttpResponse("Your account has been disabled")
        else:
            # Bad Login Details
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))
