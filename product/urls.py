from django.urls import path
from product import views

app_name = 'product'
urlpatterns = [
    path('search', views.search, name='search'),
    path('delete/<str:asin>', views.delete, name='delete'),
]
