from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Art, Photo, Comment, ProfilePhoto
from .forms import CommentForm, ProfileForm, SignUpForm

import uuid  # for generating random strings (what we name our photos)
import boto3  # sdk to interact with aws bucket

# Add these "constants" below the imports
S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'start-streetart'

class ArtCreate(LoginRequiredMixin, CreateView):
    model = Art
    fields = ['name', 'artist', 'description']

    # When valid art is added, assign a user as its owner.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class commentDelete(DeleteView):
    model = Comment
    success_url = '/'

class ArtDelete(DeleteView):
    model = Art
    success_url = '/art/'

class ArtUpdate(UpdateView):
    model = Art
    fields = '__all__'
    success_url = '/art/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def art_index(request):
    art = Art.objects.all()
    return render(request, 'art/index.html', {'art': art})

@login_required
def art_detail(request, art_id):
    oneArt = Art.objects.get(id=art_id)
    comment_form = CommentForm()
    return render(request, 'art/detail.html', {
        'oneArt': oneArt,
        'comment_form': comment_form
    })

@login_required
def add_photo(request, art_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to art_id or at (if you have an art object)
            photo = Photo(url=url, art_id=art_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('art_detail', art_id=art_id)

def delete_photo(request, art_id):
    s3 = boto3.resource('s3')
    photo = s3.Object('start-streetart', '59a0c7.jpg')
    photo.delete()
    return redirect('art_detail', art_id=art_id)

@login_required
def add_comment(request, art_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.art_id = art_id
        new_comment.save()
    return redirect('art_detail', art_id=art_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save()
            # Profile.objects.create()
            login(request, user)
            return redirect('art_index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    sign_up_form = SignUpForm()
    context = {'sign_up_form': sign_up_form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def profile_detail(request):
    profile_form = ProfileForm(instance=request.user)
    return render(request, 'profile/detail.html', {
        'user': request.user,
        'profile_form': profile_form
    })

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile_detail')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile/detail.html', {
        'user': user,
        'profile_form': profile_form
    })

@login_required
def add_profile_photo(request):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            filename = key
            profile = request.user.profile
            print(url)
            print(filename)
            print(profile)
            # we can assign to art_id or at (if you have an art object)
            photo = ProfilePhoto(url=url, filename=filename, profile=profile)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile_detail')

@login_required
def delete_profile_photo(request):
    existing_profile_photo = request.user.profile.profilephoto
    s3del = boto3.resource('s3')
    photo = s3del.Object(BUCKET, existing_profile_photo.filename)
    photo.delete()
    existing_profile_photo.delete()
    return redirect('profile_detail')