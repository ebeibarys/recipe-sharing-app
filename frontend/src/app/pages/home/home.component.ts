import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RecipeCardComponent } from '../../components/recipe-card/recipe-card.component';
import { RecipeService } from '../../services/recipe.service';
import { AuthService } from '../../services/auth.service';
import { Recipe } from '../../models/recipe.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, RecipeCardComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  featuredRecipes: Recipe[] = [];
  searchQuery = '';
  loading = false;
  error = '';

  categories = [
    { name: 'Завтрак', value: 'Завтрак', emoji: '🍳' },
    { name: 'Обед', value: 'Обед', emoji: '🥗' },
    { name: 'Ужин', value: 'Ужин', emoji: '🍝' },
    { name: 'Десерт', value: 'Десерт', emoji: '🍰' },
    { name: 'Суп', value: 'Суп', emoji: '🍲' },
    { name: 'Закуски', value: 'Закуски', emoji: '🥪' },
  ];

  constructor(
    private recipeService: RecipeService,
    public authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void { 
    this.loadFeatured(); 
  }

  loadFeatured(): void {
    this.loading = true;
    this.cdr.detectChanges();
    
    this.recipeService.getFeaturedRecipes().subscribe({
      next: recipes => { 
        this.featuredRecipes = recipes; 
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: err => { 
        this.error = err.message; 
        this.loading = false;
        this.cdr.detectChanges();
      }
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

  onLikeToggled(id: number): void {
    if (!this.authService.isLoggedIn()) { 
      this.router.navigate(['/login']); 
      return; 
    }
    this.recipeService.toggleLike(id).subscribe({
      next: res => {
        const r = this.featuredRecipes.find(x => x.id === id);
        if (r) { 
          r.is_liked = res.is_liked; 
          r.likes_count = res.likes_count;
          this.cdr.detectChanges();
        }
      }
    });
  }

  onSaveToggled(id: number): void {
    if (!this.authService.isLoggedIn()) { 
      this.router.navigate(['/login']); 
      return; 
    }
    this.recipeService.toggleSave(id).subscribe({
      next: res => { 
        const r = this.featuredRecipes.find(x => x.id === id); 
        if (r) {
          r.is_saved = res.is_saved;
          this.cdr.detectChanges();
        }
      }
    });
  }
}