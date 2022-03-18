from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect,render
from .models import Photo, Post
from .forms import Postform, PictureForm
from django.urls import reverse_lazy, reverse
from cloudinary.forms import cl_init_js_callbacks

def index(request):
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

        else:
            return HttpResponseRedirect(form.error.as_json())

    posts = Post.objects.all().order_by('-created_at')[:20]

    return render(request, 'posts.html',
                  {'posts': posts})


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(form.errors.as_json())

    form = Postform
    return render(request, 'edit.html', {'post': post, 'form': form})


def LikeView(request, post_id):
    post = Post.objects.get(id=post_id)
    new_value = post.likes + 1
    post.likes = new_value
    post.save()
    return HttpResponseRedirect('/')