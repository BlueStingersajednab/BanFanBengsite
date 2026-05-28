from django.urls import path
from . import views

urlpatterns = [
    path('gender/list', views.gender_list),
    path('gender/add', views.add_gender),
    path('gender/edit/<int:genderId>', views.edit_gender),
    path('gender/delete/<int:genderId>', views.delete_gender),
    path('user/list', views.user_list),
    path('user/add', views.add_user),
    
    path('management/indexmanage', views.dashboard_home),
    path('management/menu/', views.menu_list, name='menu_list'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/edit/<int:id>/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/delete/<int:id>/', views.delete_menu_item, name='delete_menu_item'),
]