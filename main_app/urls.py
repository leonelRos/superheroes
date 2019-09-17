from django.urls import path
from . import views
from django.contrib.auth.models import User


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup', views.signup, name='signup'),
    path('superheroes/', views.superheroes, name='superheroes'),
    path('superheroes/<int:superhero_id>/', views.superheroes_detail, name='detail'),
    path('superheroes/create/', views.SuperheroCreate.as_view(), name='superheroes_create'),
    path('superheroes/<int:pk>/update/', views.SuperheroUpdate.as_view(), name='superheroes_update'),
    path('superheroes/<int:pk>/delete/', views.SuperheroDelete.as_view(), name='superheroes_delete'),

    #heroes
    path('powers/create/', views.PowersCreate.as_view(), name='superpower_add'),
    path('powers/<int:pk>/', views.PowerDetail.as_view(), name='power_detail'),
    path('powers/<int:pk>/delete', views.PowerDelete.as_view(), name='power_delete'),
    path('powers/<int:pk>/update', views.PowerUpdate.as_view(), name='power_update'),
]

