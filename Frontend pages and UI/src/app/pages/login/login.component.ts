import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  mode: 'login' | 'register' = 'login';
  loading = false;
  error = '';
  success = '';

  loginForm = { username: '', password: '' };
  registerForm = { username: '', email: '', password: '', confirmPassword: '' };

  constructor(private authService: AuthService, private router: Router) {
    if (this.authService.isLoggedIn()) this.router.navigate(['/']);
  }

  onLogin(): void {
    this.error = '';
    if (!this.loginForm.username || !this.loginForm.password) {
      this.error = 'Заполните все поля.'; return;
    }
    this.loading = true;
    this.authService.login(this.loginForm).subscribe({
      next: () => this.router.navigate(['/']),
      error: err => { this.error = err.message; this.loading = false; }
    });
  }

  onRegister(): void {
    this.error = '';
    const f = this.registerForm;
    if (!f.username || !f.email || !f.password) {
      this.error = 'Заполните все поля.'; return;
    }
    if (f.password !== f.confirmPassword) {
      this.error = 'Пароли не совпадают.'; return;
    }
    if (f.password.length < 6) {
      this.error = 'Пароль минимум 6 символов.'; return;
    }
    this.loading = true;
    this.authService.register({ username: f.username, email: f.email, password: f.password }).subscribe({
      next: () => this.router.navigate(['/']),
      error: err => { this.error = err.message; this.loading = false; }
    });
  }

  switchMode(m: 'login' | 'register'): void {
    this.mode = m;
    this.error = '';
    this.success = '';
  }
}
