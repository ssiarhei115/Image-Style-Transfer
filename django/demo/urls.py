from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='home'),
    path('price_prediction/', views.prediction, name='price_prediction'),
    path('style_transfer/', views.stylize, name='style_transfer'),
    path('cats/<int:cat_id>/', views.categories, name='catid'),
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='catslug'),
    path('about/', views.about, name='about'),
    path('word_helper/', views.word, name='word_helper'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('admin/', admin.site.urls),
    
    #path("about/", TemplateView.as_view(template_name="about.html")),
]

# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()