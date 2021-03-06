from django.urls import path, include
import views

# In this example, we've separated out the views.py into a new file
urlpatterns = [
    path('', views.index, name="home"),
    path('about', views.about, name="about"),
    path('github', views.github, name="github"),
    path('contact', views.contact, name="contact"),
    path('services', views.services, name="services"),
    path('resume', views.resume, name="resume"),
    path('music', views.music, name="music"),

]

# Boilerplate to include static files
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
