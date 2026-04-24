import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RecipeService } from '../../services/recipe.service';
import { AuthService } from '../../services/auth.service';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-recipe-detail',
  templateUrl: './recipe-detail.component.html',
  styleUrls: ['./recipe-detail.component.css']
})
export class RecipeDetailComponent implements OnInit {
  recipe: Recipe | null = null;
  loading = false;
  error = '';
  deleteConfirm = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private recipeService: RecipeService,
    public authService: AuthService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadRecipe(id);
  }

  loadRecipe(id: number): void {
    this.loading = true;
    this.error = '';
    this.recipeService.getRecipe(id).subscribe({
      next: recipe => { this.recipe = recipe; this.loading = false; },
      error: err => { this.error = err.message; this.loading = false; }
    });
  }

  toggleFavorite(): void {
    if (!this.recipe) return;
    this.recipeService.toggleFavorite(this.recipe.id).subscribe({
      next: res => { if (this.recipe) this.recipe.is_favorite = res.is_favorite; },
      error: err => this.error = err.message
    });
  }

  deleteRecipe(): void {
    if (!this.recipe) return;
    this.recipeService.deleteRecipe(this.recipe.id).subscribe({
      next: () => this.router.navigate(['/recipes']),
      error: err => this.error = err.message
    });
  }

  isOwner(): boolean {
    const user = this.authService.getCurrentUser();
    return !!user && !!this.recipe && user.id === this.recipe.author;
  }

  getIngredientsList(): string[] {
    if (!this.recipe) return [];
    return this.recipe.ingredients.split('\n').filter(l => l.trim());
  }

  getInstructionsList(): string[] {
    if (!this.recipe) return [];
    return this.recipe.instructions.split('\n').filter(l => l.trim());
  }
}
