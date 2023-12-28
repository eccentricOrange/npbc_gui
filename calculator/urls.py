from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='calculator-home'),
    path('get_calculated_cost', views.get_calculated_cost,
         name='calculator-get-calculated-cost'),
]