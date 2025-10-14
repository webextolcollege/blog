from django.http import FileResponse, Http404
from django.conf import settings
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .models import Blog, Category, Comment
from django.db.models import Q

def posts_by_category(request, category_id):
    # Fetch the Posts that belongs to the category with the id category_id
    posts = Blog.objects.filter(status= 'Published', category=category_id)
    #try:
    #    category= Category.objects.get(pk=category_id)
    #except:
    #    return redirect('home')
    #category = Category.objects.get(pk=category_id)
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'posts': posts,
        'category': category,
        }
    return render (request, 'posts_by_category.html', context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status= 'Published')

    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = single_blog
        comment.comment = request.POST.get('comment')
        comment.save()
        return HttpResponseRedirect(request.path_info)

    # Comments
    comments = Comment.objects.filter(blog=single_blog)
    comment_count = comments.count()

    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count,
    }
    return render (request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')
    context = {
        'blogs': blogs,
        'keyword':keyword,
    }
    return render (request, 'search.html', context)

# download the pdf file

def home(request):
    context={
        'file':Blog.objects.all(),  
        
    }
    return render (request, 'blogs.html', context)


def download_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    real_path = os.path.realpath(file_path)

    # Prevent access outside MEDIA_ROOT
    if not real_path.startswith(os.path.realpath(settings.MEDIA_ROOT)):
        raise Http404("Invalid file path")

    if not os.path.exists(real_path):
        raise Http404("File not found.")

    response = FileResponse(open(real_path, 'rb'))
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(real_path)}"'
    return response






