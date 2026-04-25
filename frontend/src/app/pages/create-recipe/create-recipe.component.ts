import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RecipeService } from '../../services/recipe.service';
import { Category } from '../../models/recipe.model';

@Component({
  selector: 'app-create-recipe',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './create-recipe.component.html',
  styleUrls: ['./create-recipe.component.css']
})
export class CreateRecipeComponent implements OnInit {
  loading = false;
  error = '';
  categories: Category[] = [];

  form = {
    title: '',
    description: '',
    ingredients: '',
    instructions: '',
    cooking_time: 30,
    servings: 2,
    difficulty: 'medium' as 'easy' | 'medium' | 'hard',
    image: '',
    category: null as number | null,
  };

  constructor(private recipeService: RecipeService, private router: Router) {}

  ngOnInit(): void {
    this.recipeService.getCategories().subscribe({
      next: cats => this.categories = cats,
      error: () => {}
    });
  }

  validate(): string {
    if (!this.form.title.trim()) return 'Введите название рецепта.';
    if (!this.form.description.trim()) return 'Введите описание.';
    if (!this.form.ingredients.trim()) return 'Введите ингредиенты (каждый с новой строки).';
    if (!this.form.instructions.trim()) return 'Введите инструкции по приготовлению.';
    if (this.form.cooking_time < 1) return 'Время приготовления должно быть больше 0.';
    if (this.form.servings < 1) return 'Кол-во порций должно быть больше 0.';
    return '';
  }

  submit(): void {
    this.error = this.validate();
    if (this.error) return;

    this.loading = true;
    const payload: any = {
      title: this.form.title.trim(),
      description: this.form.description.trim(),
      ingredients: this.form.ingredients.trim(),
      instructions: this.form.instructions.trim(),
      cooking_time: this.form.cooking_time,
      servings: this.form.servings,
      difficulty: this.form.difficulty,
      image: this.form.image.trim(),
    };
    if (this.form.category) payload.category = this.form.category;

    this.recipeService.createRecipe(payload).subscribe({
      next: recipe => {
        this.loading = false;
        this.router.navigate(['/recipes', recipe.id]);
      },
      error: err => {
        this.error = err.message;
        this.loading = false;
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/recipes']);
  }
}