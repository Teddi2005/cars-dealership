from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("djangoapp.urls")),
    path("about", TemplateView.as_view(template_name="About.html"), name="about"),
    path("contact", TemplateView.as_view(template_name="Contact.html"), name="contact"),
]
