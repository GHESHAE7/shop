from django.urls import path
from .views import add_commnet


urlpatterns = [
    path('add', add_commnet, name="add_comment"),
]
