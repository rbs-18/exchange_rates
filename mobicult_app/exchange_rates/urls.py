from django.urls import path


from . import views

app_name = 'exchange_rates'

urlpatterns = [
    path('', views.index, name='index'),
]
