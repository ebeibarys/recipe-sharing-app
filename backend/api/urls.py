from django.urls import path
from .views import (
    test_api,
    category_list,
    register_user,
    RecipeListCreateView,
    RecipeDetailView,
    CommentCreateView
)

urlpatterns = [
    path('test/', test_api),

    path('categories/', category_list),
    path('register/', register_user),

    path('recipes/', RecipeListCreateView.as_view()),
    path('recipes/<int:pk>/', RecipeDetailView.as_view()),

    path('comments/', CommentCreateView.as_view()),
]