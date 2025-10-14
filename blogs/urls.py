from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve


from  .import views
from django.urls import path

urlpatterns = [
    path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    re_path(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)