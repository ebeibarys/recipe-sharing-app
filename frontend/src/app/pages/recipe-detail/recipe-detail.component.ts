import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RecipeService } from '../../services/recipe.service';
import { AuthService } from '../../services/auth.service';
import { Recipe, Comment } from '../../models/recipe.model';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-recipe-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './recipe-detail.component.html',
  styleUrls: ['./recipe-detail.component.css']
})
export class RecipeDetailComponent implements OnInit, OnDestroy {
  recipe: Recipe | null = null;
  loading = true;
  error = '';
  deleteConfirm = false;
  comments: Comment[] = [];
  newCommentText = '';
  commentLoading = false;
  commentError = '';
  private destroy$ = new Subject<void>();

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private recipeService: RecipeService,
    public authService: AuthService,
    private cdr: ChangeDetectorRef  // ← Добавлено
  ) {}

  ngOnInit(): void {
    this.route.params.pipe(takeUntil(this.destroy$)).subscribe(params => {
      const id = Number(params['id']);
      if (id && !isNaN(id)) {
        this.loadRecipe(id);
      } else {
        this.error = 'Неверный ID рецепта';
        this.loading = false;
        this.cdr.detectChanges();  // ← Добавлено
      }
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadRecipe(id: number): void {
    this.loading = true;
    this.error = '';
    this.cdr.detectChanges();  // ← Добавлено
    
    this.recipeService.getRecipe(id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (recipe) => {
          this.recipe = recipe;
          this.comments = recipe.comments || [];
          this.loading = false;
          this.cdr.detectChanges();  // ← Добавлено - ЗАСТАВЛЯЕТ ОБНОВИТЬ VIEW
        },
        error: (err) => { 
          this.error = err.message || 'Ошибка загрузки рецепта';
          this.loading = false;
          this.cdr.detectChanges();  // ← Добавлено
        }
      });
  }

  toggleLike(): void {
    if (!this.recipe) return;
    if (!this.authService.isLoggedIn()) { 
      this.router.navigate(['/login']); 
      return; 
    }
    this.recipeService.toggleLike(this.recipe.id).subscribe({
      next: res => {
        if (this.recipe) {
          this.recipe.is_liked = res.is_liked;
          this.recipe.likes_count = res.likes_count;
          this.cdr.detectChanges();  // ← Добавлено
        }
      },
      error: err => {
        this.error = err.message;
        this.cdr.detectChanges();  // ← Добавлено
      }
    });
  }

  toggleSave(): void {
    if (!this.recipe) return;
    if (!this.authService.isLoggedIn()) { 
      this.router.navigate(['/login']); 
      return; 
    }
    this.recipeService.toggleSave(this.recipe.id).subscribe({
      next: res => { 
        if (this.recipe) {
          this.recipe.is_saved = res.is_saved;
          this.cdr.detectChanges();  // ← Добавлено
        }
      },
      error: err => {
        this.error = err.message;
        this.cdr.detectChanges();  // ← Добавлено
      }
    });
  }

  deleteRecipe(): void {
    if (!this.recipe) return;
    this.recipeService.deleteRecipe(this.recipe.id).subscribe({
      next: () => {
        this.router.navigate(['/recipes']);
        this.cdr.detectChanges();  // ← Добавлено
      },
      error: err => {
        this.error = err.message;
        this.cdr.detectChanges();  // ← Добавлено
      }
    });
  }

  isOwner(): boolean {
    return !!(this.authService.getCurrentUser() && this.recipe && 
              this.authService.getCurrentUser()?.id === this.recipe.author);
  }

  getIngredientsList(): string[] {
    if (!this.recipe) return [];
    return this.recipe.ingredients.split('\n').filter(l => l.trim());
  }

  getInstructionsList(): string[] {
    if (!this.recipe) return [];
    return this.recipe.instructions.split('\n').filter(l => l.trim());
  }

  getDifficultyLabel(d: string): string {
    return d === 'easy' ? 'Лёгкий' : d === 'medium' ? 'Средний' : 'Сложный';
  }

  submitComment(): void {
    if (!this.recipe || !this.newCommentText.trim()) return;
    this.commentLoading = true;
    this.commentError = '';
    this.cdr.detectChanges();  // ← Добавлено
    
    this.recipeService.addComment(this.recipe.id, this.newCommentText.trim()).subscribe({
      next: comment => {
        this.comments.unshift(comment);
        this.newCommentText = '';
        this.commentLoading = false;
        this.cdr.detectChanges();  // ← Добавлено
      },
      error: err => { 
        this.commentError = err.message; 
        this.commentLoading = false;
        this.cdr.detectChanges();  // ← Добавлено
      }
    });
  }

  deleteComment(commentId: number): void {
    this.recipeService.deleteComment(commentId).subscribe({
      next: () => { 
        this.comments = this.comments.filter(c => c.id !== commentId);
        this.cdr.detectChanges();  // ← Добавлено
      },
      error: err => {
        this.commentError = err.message;
        this.cdr.detectChanges();  // ← Добавлено
      }
    });
  }

  isCommentOwner(comment: Comment): boolean {
    const user = this.authService.getCurrentUser();
    return !!user && user.id === comment.user;
  }

  formatDate(dateStr: string): string {
    const d = new Date(dateStr);
    return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
  }
}