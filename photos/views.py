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
        photos_all = category.photos.order_by("id")  # Returns all photos for specific category
    paginator = Paginator(photos_all, 20)  # Paginates all photos into pages of 20

    category_list = Category.objects.all()

    # Error trapping, set pages
    try:
        photos = paginator.page(page_number)
    except PageNotAnInteger:  # Page number to low
        photos = paginator.page(1)
    except EmptyPage:  # Page number to high
        photos = paginator.page(paginator.num_pages)

    # Only show page numbers if more than 1 pages.
    show_nav = paginator.num_pages >= 2

    page_list = pageinateRange(photos.number, paginator.num_pages)
    context = {
        'photos': photos,
        'page_list': page_list,
        'num_pages': paginator.num_pages,
        'category_slug': category_slug,  # Different from category - may be all
        'category': category,
        'categories': category_list,
        'show_nav': show_nav
    }

    request.session['page'] = photos.number
    request.session['category'] = category_slug
    

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

            # Gets session data - returns user to page they were before entering the form
            page = request.session.get('page','1') 
            category = request.session.get('category','all')

            return redirect(reverse('index', args=(category,page)))
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


def pageinateRange(current, lastpage):
    firstpage = 1
    # If 10 or less pages, just return normal page numbers
    if lastpage <= 10:
        return list(range(firstpage, lastpage + 1))

    lowerBound = current - 5  # The first number to display
    upperBound = current + 4  # The last number

    # Check if the lower bound is lower than the first page number
    if lowerBound < firstpage:
        # if it is, give an extra "buffer" to the upper bound - always shows 10 numbers
        upperAdd = firstpage - lowerBound
        upperBound += upperAdd
        lowerBound = firstpage

    # Check if the upper bound set exceeds the number of pages
    if upperBound > lastpage:
        # if it is, give an extra "buffer" to the lower bound - always shows 10 numbers
        lowerAdd = lastpage - upperBound
        lowerBound += lowerAdd
        upperBound = lastpage

    return list(range(lowerBound, upperBound + 1))
