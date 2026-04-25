from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from .models import Category, Recipe, Comment, Like, SavedRecipe
from .serializers import (
    CategorySerializer,
    RecipeSerializer,
    RecipeListSerializer,
    CommentSerializer,
    SavedRecipeSerializer,
    RegisterSerializer,
    LoginSerializer,
)


# Pagination for recipes
class RecipePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50


# Auth endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data.get('email', ''),
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {'id': user.id, 'username': user.username, 'email': user.email}
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
    )
    if not user:
        return Response({'detail': 'Неверное имя пользователя или пароль.'}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({'detail': 'Вы вышли из системы.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({'id': user.id, 'username': user.username, 'email': user.email})


# Categories
@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all()
    return Response(CategorySerializer(categories, many=True).data)


# Recipes List and Create
class RecipeListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        qs = Recipe.objects.select_related('author', 'category').prefetch_related('likes', 'saved_by')

        # Search
        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(title__icontains=search)

        # Category filter
        category = request.query_params.get('category', '').strip()
        if category:
            if category.isdigit():
                qs = qs.filter(category_id=category)
            else:
                qs = qs.filter(category__name__iexact=category)

        # Difficulty filter
        difficulty = request.query_params.get('difficulty', '').strip()
        if difficulty in ('easy', 'medium', 'hard'):
            qs = qs.filter(difficulty=difficulty)

        qs = qs.order_by('-created_at')
        
        # Pagination
        paginator = RecipePagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = RecipeListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Featured recipes (limited to 6)
@api_view(['GET'])
@permission_classes([AllowAny])
def featured_recipes(request):
    qs = (Recipe.objects
          .select_related('author', 'category')
          .prefetch_related('likes', 'saved_by')
          .order_by('-created_at')[:6])
    serializer = RecipeListSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


# Recipe Detail
class RecipeDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Recipe.objects.select_related('author', 'category').prefetch_related(
                'likes', 'saved_by', 'comments__user'
            ).get(pk=pk)
        except Recipe.DoesNotExist:
            return None

    def get(self, request, pk):
        recipe = self.get_object(pk)
        if not recipe:
            return Response({'detail': 'Рецепт не найден.'}, status=404)
        return Response(RecipeSerializer(recipe, context={'request': request}).data)

    def put(self, request, pk):
        recipe = self.get_object(pk)
        if not recipe:
            return Response({'detail': 'Рецепт не найден.'}, status=404)
        if recipe.author != request.user:
            return Response({'detail': 'Нет доступа.'}, status=403)
        serializer = RecipeSerializer(recipe, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        recipe = self.get_object(pk)
        if not recipe:
            return Response({'detail': 'Рецепт не найден.'}, status=404)
        if recipe.author != request.user:
            return Response({'detail': 'Нет доступа.'}, status=403)
        recipe.delete()
        return Response({'detail': 'Рецепт удалён.'}, status=204)


# Like / Save
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response({'detail': 'Рецепт не найден.'}, status=404)

    like, created = Like.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True

    return Response({'is_liked': is_liked, 'likes_count': recipe.likes.count()})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_save(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response({'detail': 'Рецепт не найден.'}, status=404)

    saved, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        saved.delete()
        is_saved = False
    else:
        is_saved = True

    return Response({'is_saved': is_saved})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saved_recipes(request):
    saved = SavedRecipe.objects.filter(user=request.user).select_related('recipe__author', 'recipe__category')
    serializer = SavedRecipeSerializer(saved, many=True, context={'request': request})
    return Response(serializer.data)


# Comments
class CommentListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        recipe_id = request.query_params.get('recipe')
        qs = Comment.objects.select_related('user')
        if recipe_id:
            qs = qs.filter(recipe_id=recipe_id)
        qs = qs.order_by('-created_at')[:20]  # Limit comments
        return Response(CommentSerializer(qs, many=True).data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({'detail': 'Комментарий не найден.'}, status=404)
    if comment.user != request.user:
        return Response({'detail': 'Нет доступа.'}, status=403)
    comment.delete()
    return Response({'detail': 'Комментарий удалён.'}, status=204)


# Test
@api_view(['GET'])
@permission_classes([AllowAny])
def test_api(request):
    return Response({"message": "Recipe API works ✓"})