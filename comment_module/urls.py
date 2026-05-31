from django.urls import path
from .views import add_commnet

app_name = "comment_module"

urlpatterns = [
    path("add", add_commnet, name="add_comment"),
]
