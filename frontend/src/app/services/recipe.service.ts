import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, throwError, of, map } from 'rxjs';
import { Recipe, Comment, Category } from '../models/recipe.model';

@Injectable({ providedIn: 'root' })
export class RecipeService {
  private apiUrl = 'http://localhost:8000/api';
  private recipeCache = new Map<number, Recipe>();

  constructor(private http: HttpClient) {}

  getRecipes(search?: string, category?: string, difficulty?: string): Observable<Recipe[]> {
    const params: string[] = [];
    if (search) params.push(`search=${encodeURIComponent(search)}`);
    if (category) params.push(`category=${encodeURIComponent(category)}`);
    if (difficulty) params.push(`difficulty=${encodeURIComponent(difficulty)}`);
    const query = params.length ? '?' + params.join('&') : '';
    
    // Handle paginated response
    return this.http.get<any>(`${this.apiUrl}/recipes/${query}`).pipe(
      map(response => {
        // If response has results property (paginated), return results
        if (response && response.results) {
          return response.results as Recipe[];
        }
        // If response is array, return as is
        return response as Recipe[];
      }),
      catchError(this.handleError)
    );
  }

  getRecipe(id: number): Observable<Recipe> {
    if (this.recipeCache.has(id)) {
      return of(this.recipeCache.get(id)!);
    }
    
    return this.http.get<Recipe>(`${this.apiUrl}/recipes/${id}/`).pipe(
      catchError(this.handleError)
    );
  }

  getFeaturedRecipes(): Observable<Recipe[]> {
    return this.http.get<Recipe[]>(`${this.apiUrl}/recipes/featured/`).pipe(
      catchError(this.handleError)
    );
  }

  createRecipe(data: Partial<Recipe>): Observable<Recipe> {
    return this.http.post<Recipe>(`${this.apiUrl}/recipes/`, data).pipe(catchError(this.handleError));
  }

  updateRecipe(id: number, data: Partial<Recipe>): Observable<Recipe> {
    return this.http.patch<Recipe>(`${this.apiUrl}/recipes/${id}/`, data).pipe(catchError(this.handleError));
  }

  deleteRecipe(id: number): Observable<void> {
    this.recipeCache.delete(id);
    return this.http.delete<void>(`${this.apiUrl}/recipes/${id}/`).pipe(catchError(this.handleError));
  }

  toggleLike(id: number): Observable<{ is_liked: boolean; likes_count: number }> {
    return this.http.post<{ is_liked: boolean; likes_count: number }>(`${this.apiUrl}/recipes/${id}/like/`, {})
      .pipe(catchError(this.handleError));
  }

  toggleSave(id: number): Observable<{ is_saved: boolean }> {
    return this.http.post<{ is_saved: boolean }>(`${this.apiUrl}/recipes/${id}/save/`, {})
      .pipe(catchError(this.handleError));
  }

  getSavedRecipes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/saved/`).pipe(catchError(this.handleError));
  }

  getComments(recipeId: number): Observable<Comment[]> {
    return this.http.get<Comment[]>(`${this.apiUrl}/comments/?recipe=${recipeId}`).pipe(catchError(this.handleError));
  }

  addComment(recipeId: number, text: string): Observable<Comment> {
    return this.http.post<Comment>(`${this.apiUrl}/comments/`, { text, recipe: recipeId }).pipe(catchError(this.handleError));
  }

  deleteComment(commentId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/comments/${commentId}/`).pipe(catchError(this.handleError));
  }

  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.apiUrl}/categories/`).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse) {
    let message = 'Произошла ошибка. Попробуйте снова.';
    if (error.status === 401) message = 'Необходима авторизация.';
    else if (error.status === 403) message = 'Нет доступа.';
    else if (error.status === 404) message = 'Не найдено.';
    else if (error.status === 0) message = 'Сервер недоступен. Проверьте соединение.';
    else if (error.error?.detail) message = error.error.detail;
    else if (typeof error.error === 'string') message = error.error;
    return throwError(() => new Error(message));
  }
}