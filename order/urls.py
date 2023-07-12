from django.urls import path
from order import views
urlpatterns = [
    path('', views.CreateOrderView.as_view()),
    path('<pk>/', views.CreateOrderView.as_view()),
]