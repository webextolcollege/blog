from django.shortcuts import get_object_or_404, render
from blogs.models import Blog, Category, Comment
from django.contrib.auth.decorators import login_required
from .forms import AddUserForm, BlogPostForm, CategoryForm
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .models import Post
from django.http import HttpResponse, HttpResponseRedirect


from django.http import FileResponse, Http404
from django.conf import settings
import os

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
    'category_count':category_count,
    'blogs_count': blogs_count,
}
    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    return render(request, 'dashboard/categories.html')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_category.html', context)

def edit_category(request, pk):
    category =get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories') #Redirect to the categories page after a successful update
    else:
        form = CategoryForm(instance = category)
    context= {
        'form': form,
        'category': category,
    
    }
    return render(request, 'dashboard/edit_category.html', context)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts = Blog.objects.all()
    context={
        'posts': posts
    }
    return render(request, 'dashboard/posts.html', context)
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  #temporary saving the form
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
        else:
            print('form is invalid')
            print(form.errors)
    form=BlogPostForm()
    context={
        'form': form, 
    }
    return render(request, 'dashboard/add_post.html', context)

def edit_post(request, pk):
    post=get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post=form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    form=BlogPostForm(instance=post)
    context = {
        'form': form,
        'post': post,
        }
    return render(request, 'dashboard/edit_post.html', context)

def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')

def users(request):
    users = User.objects.all()
    context={
        'users': users
    }

    return render(request, 'dashboard/users.html', context)

def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
    form = AddUserForm()
    context = {
        'form': form,
    }
    
    return render(request, 'dashboard/add_user.html', context )
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = AddUserForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'dashboard/edit_user.html', context)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')





# Post details
def post_detail(request, post_slug):
    single_post = get_object_or_404(Blog, slug=post_slug, status='Published')
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = single_post
        comment.comment = request.POST.get('comment')
        comment.save()
        return HttpResponseRedirect(request.path_info)

    # Comments
    comments = Comment.objects.filter(blog=single_post)
    comment_count = comments.count()

    context = {
        'single_post': single_post,
        'comments': comments,
        'comment_count': comment_count,

    }

    return render(request, 'dashboard/post_detail.html', context)

# pdf file download
def home(request):
    context={
        'file':Post.objects.all(),  
        
    }
    return render (request, 'post_detail.html', context)


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

