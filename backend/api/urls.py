from django.urls import path
from .views import (
    test_api,
    register_user,
    login_user,
    logout_user,
    me,
    category_list,
    RecipeListCreateView,
    RecipeDetailView,
    featured_recipes,
    toggle_like,
    toggle_save,
    saved_recipes,
    CommentListCreateView,
    delete_comment,
)

urlpatterns = [
    path('test/', test_api),

    # Auth
    path('auth/register/', register_user),
    path('auth/login/', login_user),
    path('auth/logout/', logout_user),
    path('auth/me/', me),

    # Categories
    path('categories/', category_list),

    # Recipes
    path('recipes/', RecipeListCreateView.as_view()),
    path('recipes/featured/', featured_recipes),
    path('recipes/<int:pk>/', RecipeDetailView.as_view()),
    path('recipes/<int:pk>/like/', toggle_like),
    path('recipes/<int:pk>/save/', toggle_save),

    # Saved
    path('saved/', saved_recipes),

    # Comments
    path('comments/', CommentListCreateView.as_view()),
    path('comments/<int:pk>/', delete_comment),
]
