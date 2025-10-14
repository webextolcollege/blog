from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name
    
STATUS_CHOICES = (
    ("Draft", "Draft"),
    ("Published", "Published")
)

class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    auther = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    featured_image = models.ImageField(upload_to='uploads/%y/%m/%d')
    short_description = HTMLField()
    blog_body = HTMLField()
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices = STATUS_CHOICES, default = "Draft")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models. DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models. DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
