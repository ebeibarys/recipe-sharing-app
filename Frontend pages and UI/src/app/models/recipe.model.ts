export interface Recipe {
  id: number;
  title: string;
  description: string;
  ingredients: string;
  instructions: string;
  cooking_time: number;
  servings: number;
  category: string;
  image?: string;
  author: number;
  author_name?: string;
  created_at: string;
  is_favorite?: boolean;
}

export interface RecipeCreate {
  title: string;
  description: string;
  ingredients: string;
  instructions: string;
  cooking_time: number;
  servings: number;
  category: string;
  image?: File;
}

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}
