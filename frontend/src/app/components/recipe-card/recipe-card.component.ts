import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-recipe-card',
  standalone: true,
  imports: [RouterLink, CommonModule],
  templateUrl: './recipe-card.component.html',
  styleUrls: ['./recipe-card.component.css']
})
export class RecipeCardComponent {
  @Input() recipe!: Recipe;
  @Output() likeToggled = new EventEmitter<number>();
  @Output() saveToggled = new EventEmitter<number>();

  onLike(event: Event): void {
    event.stopPropagation();
    event.preventDefault();
    this.likeToggled.emit(this.recipe.id);
  }

  onSave(event: Event): void {
    event.stopPropagation();
    event.preventDefault();
    this.saveToggled.emit(this.recipe.id);
  }

  getCategoryEmoji(category: string): string {
    const map: Record<string, string> = {
      'Завтрак': '🍳', 'Обед': '🥗', 'Ужин': '🍝',
      'Десерт': '🍰', 'Закуски': '🥪', 'Суп': '🍲',
      breakfast: '🍳', lunch: '🥗', dinner: '🍝',
      dessert: '🍰', snack: '🥪', soup: '🍲'
    };
    return map[category] || '🍽️';
  }

  getDifficultyLabel(d: string): string {
    return d === 'easy' ? 'Лёгкий' : d === 'medium' ? 'Средний' : 'Сложный';
  }

  getDifficultyClass(d: string): string {
    return `diff-${d}`;
  }
}