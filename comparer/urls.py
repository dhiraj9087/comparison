# comparer/urls.py
from django.urls import path
from .views import search_view

urlpatterns = [
    path('search/', search_view, name='search'),
    # path('search_results/', search_results_view, name='search_results'),
]
