import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-recipe-card',
  templateUrl: './recipe-card.component.html',
  styleUrls: ['./recipe-card.component.css']
})
export class RecipeCardComponent {
  @Input() recipe!: Recipe;
  @Output() favoriteToggled = new EventEmitter<number>();

  onFavorite(event: Event): void {
    event.stopPropagation();
    event.preventDefault();
    this.favoriteToggled.emit(this.recipe.id);
  }

  getCategoryEmoji(category: string): string {
    const map: Record<string, string> = {
      breakfast: '🍳', lunch: '🥗', dinner: '🍝',
      dessert: '🍰', snack: '🥪', soup: '🍲', other: '🍽️'
    };
    return map[category.toLowerCase()] || '🍽️';
  }
}
