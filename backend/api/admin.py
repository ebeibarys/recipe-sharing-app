from django.contrib import admin
from .models import Category, Recipe, Comment, SavedRecipe

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(SavedRecipe)