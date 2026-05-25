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
    path('order/list', views.order_list),
    path('order/add', views.add_order),
    path('order/detail/<int:orderId>', views.order_detail),
    path('order/add-item/<int:orderId>', views.add_order_item),
    path('order/update-status/<int:orderId>', views.update_order_status),
    path('order/delete/<int:orderId>', views.delete_order),
    path('reservation/list', views.reservation_list),
    path('reservation/add', views.add_reservation),
    path('reservation/edit/<int:reservationId>', views.edit_reservation),
    path('reservation/delete/<int:reservationId>', views.delete_reservation),
    path('bill/list', views.bill_list),
    path('bill/detail/<int:billId>', views.bill_detail),
    path('bill/pay/<int:billId>', views.process_payment),
]