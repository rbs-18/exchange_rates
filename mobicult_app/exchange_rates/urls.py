from django.urls import path


from . import views

app_name = 'exchange_rates'

urlpatterns = [
    path('', views.index, name='index'),
    path('yesterday/', views.yesterday, name='yesterday'),
    path('day_before_yesterday/', views.day_before_yesterday, name='day_before_yesterday'),
]
