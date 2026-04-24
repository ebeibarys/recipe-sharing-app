import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { Recipe, RecipeCreate } from '../models/recipe.model';

@Injectable({ providedIn: 'root' })
export class RecipeService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getRecipes(search?: string, category?: string): Observable<Recipe[]> {
    let url = `${this.apiUrl}/recipes/`;
    const params: string[] = [];
    if (search) params.push(`search=${encodeURIComponent(search)}`);
    if (category) params.push(`category=${encodeURIComponent(category)}`);
    if (params.length) url += '?' + params.join('&');
    return this.http.get<Recipe[]>(url).pipe(catchError(this.handleError));
  }

  getRecipe(id: number): Observable<Recipe> {
    return this.http.get<Recipe>(`${this.apiUrl}/recipes/${id}/`).pipe(catchError(this.handleError));
  }

  createRecipe(data: RecipeCreate): Observable<Recipe> {
    const formData = new FormData();
    Object.entries(data).forEach(([key, val]) => {
      if (val !== undefined) formData.append(key, val as any);
    });
    return this.http.post<Recipe>(`${this.apiUrl}/recipes/`, formData).pipe(catchError(this.handleError));
  }

  updateRecipe(id: number, data: Partial<RecipeCreate>): Observable<Recipe> {
    return this.http.patch<Recipe>(`${this.apiUrl}/recipes/${id}/`, data).pipe(catchError(this.handleError));
  }

  deleteRecipe(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/recipes/${id}/`).pipe(catchError(this.handleError));
  }

  getFeaturedRecipes(): Observable<Recipe[]> {
    return this.http.get<Recipe[]>(`${this.apiUrl}/recipes/featured/`).pipe(catchError(this.handleError));
  }

  toggleFavorite(id: number): Observable<{ is_favorite: boolean }> {
    return this.http.post<{ is_favorite: boolean }>(`${this.apiUrl}/recipes/${id}/favorite/`, {}).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse) {
    let message = 'Произошла ошибка. Попробуйте снова.';
    if (error.status === 401) message = 'Необходима авторизация.';
    else if (error.status === 404) message = 'Не найдено.';
    else if (error.status === 0) message = 'Сервер недоступен. Проверьте соединение.';
    else if (error.error?.detail) message = error.error.detail;
    return throwError(() => new Error(message));
  }
}
