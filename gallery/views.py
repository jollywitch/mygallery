from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .models import Image
from .forms import ImageUploadForm, UserRegisterForm


def gallery_view(request):
    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.user = request.user
                image.save()
                messages.success(request, 'Image uploaded successfully!')
                return redirect('gallery')
            else:
                messages.error(request, 'Please upload a valid image file.')
        else:
            form = ImageUploadForm()
    
    images = Image.objects.all()
    context = {
        'form': form,
        'images': images,
    }
    return render(request, 'gallery/gallery.html', context)


def download_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    response = FileResponse(image.image.open(), as_attachment=True)
    return response


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    
    if image.user != request.user:
        messages.error(request, 'You can only delete your own images.')
        return redirect('gallery')
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully!')
        return redirect('gallery')
    
    return render(request, 'gallery/confirm_delete.html', {'image': image})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('gallery')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'gallery/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'gallery/register.html', {'form': form})
