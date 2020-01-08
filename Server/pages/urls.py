from django.urls import path

from pages import views
from .views import homePageView

from django.views.generic.base import TemplateView

urlpatterns = [
    path('', homePageView, name='home'),
    path('index',views.index, name='index'),
    path('about',TemplateView.as_view(template_name='about.html'), name='about'),
]