from django.urls import path


from . import views

urlpatterns = [
    path('locations', views.location_list),
    path('locations/<int:id>', views.location_detail),
    path('holidays', views.holiday_list),
    path('holidays/<int:id>', views.holiday_detail),
    path('reservations', views.reservation_list),
    path('reservations/<int:id>', views.reservation_detail),
    path('travel-agency/find-reservation', views.find_reservation),

]
