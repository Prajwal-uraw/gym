export interface User {
  user_id: string;
  email: string;
  phone?: string;
  age: number;
  gender: string;
  height: number;
  weight: number;
  fitness_goal: string;
  workout_days_per_week: number;
  diet_preference: string;
  food_allergies: string[];
  health_conditions: string[];
  created_at: string;
}

export interface Exercise {
  name: string;
  sets: number;
  reps: string;
  rest_seconds: number;
}

export interface WorkoutDay {
  day: string;
  focus: string;
  exercises: Exercise[];
}

export interface WorkoutPlan {
  weekly_schedule: WorkoutDay[];
  difficulty_level: string;
  total_duration: number;
  safety_tips: string[];
}

export interface Meal {
  meal: string;
  foods: string[];
  calories: number;
  time: string;
}

export interface DietPlan {
  daily_calories: number;
  meals: Meal[];
  macros: {
    protein: number;
    carbs: number;
    fats: number;
  };
  dietary_notes: string[];
}

export interface ProgressRecord {
  user_id: string;
  weight?: number;
  completed_workouts: string[];
  feedback?: string;
  date: string;
  created_at: string;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password?: string) => Promise<void>;
  signup: (userData: SignupData) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

export interface SignupData {
  email: string;
  phone?: string;
  password?: string;
  age: number;
  gender: string;
  height: number;
  weight: number;
  fitness_goal: string;
  workout_days_per_week: number;
  diet_preference: string;
  food_allergies: string[];
  health_conditions: string[];
}

export interface Recommendation {
  title: string;
  description: string;
  link?: string;
}

export interface RecommendationsResponse {
  recommendations: Recommendation[];
  success: boolean;
  message?: string;
}
