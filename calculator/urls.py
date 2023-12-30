from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='calculator-home'),
    path('register-undelivered-date/', views.register_undelivered_date, name='register-undelivered-date'),
    path('unregister-undelivered-date/', views.unregister_undelivered_date, name='unregister-undelivered-date'),
    path('get-calculated-costs/', views.get_calculated_costs, name='get-calculated-costs'),
    path('get-calculated-string/', views.get_calculated_string, name='get-calculated-string'),
]