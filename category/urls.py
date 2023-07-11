from django.urls import path
from category import views
urlpatterns = [
    path('', views.CategoryCreateListView.as_view()),
    path('<pk>/', views.CategoryDetailView.as_view()),
]