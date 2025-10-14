from django.contrib import admin

from .models import Blog, Category, Comment

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

    list_display = ('title', 'category', 'auther','pdf_file', 'status', 'is_featured',)
    search_fields = ('id', 'title', 'category__category__name', 'status',)
    list_editable = ('is_featured', )

admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
