import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RecipeService } from '../../services/recipe.service';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  featuredRecipes: Recipe[] = [];
  searchQuery = '';
  loading = false;
  error = '';

  categories = [
    { name: 'Завтрак', value: 'breakfast', emoji: '🍳' },
    { name: 'Обед', value: 'lunch', emoji: '🥗' },
    { name: 'Ужин', value: 'dinner', emoji: '🍝' },
    { name: 'Десерт', value: 'dessert', emoji: '🍰' },
    { name: 'Суп', value: 'soup', emoji: '🍲' },
    { name: 'Закуски', value: 'snack', emoji: '🥪' },
  ];

  constructor(private recipeService: RecipeService, private router: Router) {}

  ngOnInit(): void {
    this.loadFeatured();
  }

  loadFeatured(): void {
    this.loading = true;
    this.error = '';
    this.recipeService.getFeaturedRecipes().subscribe({
      next: recipes => { this.featuredRecipes = recipes; this.loading = false; },
      error: err => { this.error = err.message; this.loading = false; }
    });
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.router.navigate(['/recipes'], { queryParams: { search: this.searchQuery } });
    }
  }

  browseCategory(category: string): void {
    this.router.navigate(['/recipes'], { queryParams: { category } });
  }

  onFavoriteToggled(id: number): void {
    this.recipeService.toggleFavorite(id).subscribe({
      next: res => {
        const r = this.featuredRecipes.find(x => x.id === id);
        if (r) r.is_favorite = res.is_favorite;
      },
      error: err => this.error = err.message
    });
  }
}
