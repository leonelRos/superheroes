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
    path('superheroes/<int:superhero_id>/assoc_power/<int:power_id>/', views.assoc_power, name='assoc_power'),
    path('superheroes/<int:superhero_id>/unassoc_power/<int:power_id>/', views.unassoc_power, name='unassoc_power'),


    #heroes
    path('powers/', views.PowerList.as_view(), name='powers_index'),
    path('powers/create/', views.PowerCreate.as_view(), name='powers_add'),
    path('powers/<int:pk>/', views.PowerDetail.as_view(), name='powers_detail'),
    path('powers/<int:pk>/delete', views.PowerDelete.as_view(), name='powers_delete'),
    path('powers/<int:pk>/update', views.PowerUpdate.as_view(), name='powers_update'),
    path('superheroes/<int:superhero_id>/add_photo/', views.add_photo, name='add_photo'),
    path('photos/<int:pk>/delete', views.PhotoDelete.as_view(), name='photos_delete'),
    
   
    

]

