import { SignupData, User, WorkoutPlan, DietPlan, ProgressRecord, RecommendationsResponse} from '@/types';

const API_BASE_URL = 'http://localhost:8080';

class ApiClient {
  private baseURL: string;
  private token: string | null;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('auth_token');
  }

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async signup(userData: SignupData) {
    const response = await this.request<{
      access_token: string;
      user_id: string;
      message: string;
    }>('/signup', {
      method: 'POST',
      body: JSON.stringify(userData),
    });

    this.setToken(response.access_token);
    return response;
  }

  async login(email: string, password?: string) {
    const response = await this.request<{
      access_token: string;
      user_id: string;
      message: string;
    }>('/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    this.setToken(response.access_token);
    return response;
  }

  async getProfile(): Promise<User> {
    return this.request<User>('/profile');
  }

  async getWorkoutPlan(): Promise<{ workout_plan: WorkoutPlan; generated_at: string }> {
    return this.request<{ workout_plan: WorkoutPlan; generated_at: string }>('/workout-plan');
  }

  async getDietPlan(): Promise<{ diet_plan: DietPlan; generated_at: string }> {
    return this.request<{ diet_plan: DietPlan; generated_at: string }>('/diet-plan');
  }

  async getRecommendations(): Promise<RecommendationsResponse> {
  return this.request<RecommendationsResponse>("/recommendations", {
    method: "POST",
  });
}


  async submitFeedback(progressData: {
    weight?: number;
    completed_workouts: string[];
    feedback?: string;
  }) {
    return this.request<{ message: string; progress_id: string }>('/feedback', {
      method: 'POST',
      body: JSON.stringify({
        ...progressData,
        user_id: '', // Will be set by backend from token
      }),
    });
  }

  async getProgress(): Promise<{ progress: ProgressRecord[] }> {
    return this.request<{ progress: ProgressRecord[] }>('/progress');
  }

  logout() {
    this.setToken(null);
  }
}

export const apiClient = new ApiClient();