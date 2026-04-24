import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RecipeService } from '../../services/recipe.service';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-recipes',
  templateUrl: './recipes.component.html',
  styleUrls: ['./recipes.component.css']
})
export class RecipesComponent implements OnInit {
  recipes: Recipe[] = [];
  loading = false;
  error = '';
  searchQuery = '';
  selectedCategory = '';

  categories = [
    { label: 'Все', value: '' },
    { label: 'Завтрак', value: 'breakfast' },
    { label: 'Обед', value: 'lunch' },
    { label: 'Ужин', value: 'dinner' },
    { label: 'Десерт', value: 'dessert' },
    { label: 'Суп', value: 'soup' },
    { label: 'Закуски', value: 'snack' },
  ];

  constructor(
    private recipeService: RecipeService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.searchQuery = params['search'] || '';
      this.selectedCategory = params['category'] || '';
      this.loadRecipes();
    });
  }

  loadRecipes(): void {
    this.loading = true;
    this.error = '';
    this.recipeService.getRecipes(this.searchQuery, this.selectedCategory).subscribe({
      next: recipes => { this.recipes = recipes; this.loading = false; },
      error: err => { this.error = err.message; this.loading = false; }
    });
  }

  onSearch(): void {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { search: this.searchQuery || null, category: this.selectedCategory || null },
      queryParamsHandling: 'merge'
    });
  }

  selectCategory(cat: string): void {
    this.selectedCategory = cat;
    this.onSearch();
  }

  onFavoriteToggled(id: number): void {
    this.recipeService.toggleFavorite(id).subscribe({
      next: res => {
        const r = this.recipes.find(x => x.id === id);
        if (r) r.is_favorite = res.is_favorite;
      },
      error: err => this.error = err.message
    });
  }

  clearFilters(): void {
    this.searchQuery = '';
    this.selectedCategory = '';
    this.onSearch();
  }
}
