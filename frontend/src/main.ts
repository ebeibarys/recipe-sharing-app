import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter, Routes } from '@angular/router';
import { provideHttpClient, withInterceptorsFromDi, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { AuthInterceptor } from './app/interceptors/auth.interceptor';
import { AuthGuard } from './app/guards/auth.guard';

const routes: Routes = [
  { path: '', loadComponent: () => import('./app/pages/home/home.component').then(m => m.HomeComponent) },
  { path: 'login', loadComponent: () => import('./app/pages/login/login.component').then(m => m.LoginComponent) },
  { path: 'recipes', loadComponent: () => import('./app/pages/recipes/recipes.component').then(m => m.RecipesComponent) },
  { path: 'recipes/create', loadComponent: () => import('./app/pages/create-recipe/create-recipe.component').then(m => m.CreateRecipeComponent), canActivate: [AuthGuard] },
  { path: 'recipes/:id', loadComponent: () => import('./app/pages/recipe-detail/recipe-detail.component').then(m => m.RecipeDetailComponent) },
  { path: '**', redirectTo: '' }
];

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptorsFromDi()),
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ]
}).catch(err => console.error(err));