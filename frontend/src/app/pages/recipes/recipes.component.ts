import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RecipeCardComponent } from '../../components/recipe-card/recipe-card.component';
import { RecipeService } from '../../services/recipe.service';
import { AuthService } from '../../services/auth.service';
import { Recipe } from '../../models/recipe.model';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-recipes',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, RecipeCardComponent],
  templateUrl: './recipes.component.html',
  styleUrls: ['./recipes.component.css']
})
export class RecipesComponent implements OnInit, OnDestroy {
  recipes: Recipe[] = [];
  loading = false;
  error = '';
  searchQuery = '';
  selectedCategory = '';
  selectedDifficulty = '';
  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  categories = [
    { label: 'Все', value: '' },
    { label: 'Завтрак', value: 'Завтрак' },
    { label: 'Обед', value: 'Обед' },
    { label: 'Ужин', value: 'Ужин' },
    { label: 'Десерт', value: 'Десерт' },
    { label: 'Суп', value: 'Суп' },
    { label: 'Салат', value: 'Салат' },
  ];

  difficulties = [
    { label: 'Любой', value: '' },
    { label: 'Лёгкий', value: 'easy' },
    { label: 'Средний', value: 'medium' },
    { label: 'Сложный', value: 'hard' },
  ];

  constructor(
    private recipeService: RecipeService,
    public authService: AuthService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef  // ← Добавлено
  ) {}

  ngOnInit(): void {
    this.searchSubject.pipe(
      debounceTime(500),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      this.applyFilters();
    });

    this.route.queryParams.subscribe(params => {
      this.searchQuery = params['search'] || '';
      this.selectedCategory = params['category'] || '';
      this.selectedDifficulty = params['difficulty'] || '';
      this.loadRecipes();
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onSearchInput(): void {
    this.searchSubject.next(this.searchQuery);
  }

  loadRecipes(): void {
    this.loading = true;
    this.error = '';
    this.cdr.detectChanges();  // ← Добавлено
    
    this.recipeService.getRecipes(this.searchQuery, this.selectedCategory, this.selectedDifficulty).subscribe({
      next: (data: any) => {
        if (data && Array.isArray(data)) {
          this.recipes = data;
        } else if (data && data.results && Array.isArray(data.results)) {
          this.recipes = data.results;
        } else {
          this.recipes = [];
        }
        this.loading = false;
        this.cdr.detectChanges();  // ← Добавлено
      },
      error: err => { 
        this.error = err.message; 
        this.loading = false;
        this.recipes = [];
        this.cdr.detectChanges();  // ← Добавлено
      }
    });
  }

  applyFilters(): void {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        search: this.searchQuery || null,
        category: this.selectedCategory || null,
        difficulty: this.selectedDifficulty || null,
      },
      queryParamsHandling: 'merge'
    });
  }

  selectCategory(cat: string): void {
    this.selectedCategory = cat;
    this.applyFilters();
  }

  selectDifficulty(d: string): void {
    this.selectedDifficulty = d;
    this.applyFilters();
  }

  clearFilters(): void {
    this.searchQuery = '';
    this.selectedCategory = '';
    this.selectedDifficulty = '';
    this.applyFilters();
  }

  hasFilters(): boolean {
    return !!(this.searchQuery || this.selectedCategory || this.selectedDifficulty);
  }

  onLikeToggled(id: number): void {
    if (!this.authService.isLoggedIn()) { 
      this.router.navigate(['/login']); 
      return; 
    }
    this.recipeService.toggleLike(id).subscribe({
      next: res => {
        const r = this.recipes.find(x => x.id === id);
        if (r) { 
          r.is_liked = res.is_liked; 
          r.likes_count = res.likes_count;
          this.cdr.detectChanges();  // ← Добавлено
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
        const r = this.recipes.find(x => x.id === id); 
        if (r) {
          r.is_saved = res.is_saved;
          this.cdr.detectChanges();  // ← Добавлено
        }
      }
    });
  }
}