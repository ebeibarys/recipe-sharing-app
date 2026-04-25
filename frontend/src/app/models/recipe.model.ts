export interface Recipe {
  id: number;
  title: string;
  description: string;
  ingredients: string;
  instructions: string;
  cooking_time: number;
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
  image?: string;
  author: number;
  author_name?: string;
  category?: number;
  category_name?: string;
  created_at: string;
  likes_count: number;
  is_liked?: boolean;
  is_saved?: boolean;
  comments?: Comment[];
}

export interface Comment {
  id: number;
  text: string;
  created_at: string;
  user: number;
  user_name: string;
  recipe: number;
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

export interface Category {
  id: number;
  name: string;
}
