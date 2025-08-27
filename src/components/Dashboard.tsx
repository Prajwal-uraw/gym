import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Calendar } from '@/components/ui/calendar';
import { useAuth } from '@/contexts/AuthContext';
import { apiClient } from '@/lib/api';
import Chatbot from '@/components/ui/Chatbot';

import { WorkoutPlan, DietPlan, ProgressRecord, Recommendation,RecommendationsResponse} from '@/types';
import { 
  Dumbbell, 
  Apple, 
  TrendingUp, 
  Clock, 
  Target, 
  Calendar as CalendarIcon,
  User,
  LogOut
} from 'lucide-react';
import { toast } from 'sonner';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [workoutPlan, setWorkoutPlan] = useState<WorkoutPlan | null>(null);
  const [dietPlan, setDietPlan] = useState<DietPlan | null>(null);
  const [progressRecords, setProgressRecords] = useState<ProgressRecord[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());
  const [loading, setLoading] = useState(false);
  const [completedWorkouts, setCompletedWorkouts] = useState<string[]>([]);
  const [chatOpen, setChatOpen] = useState(false);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);


  useEffect(() => {
    loadData();
    loadRecommendations();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [workoutResponse, dietResponse, progressResponse] = await Promise.all([
        apiClient.getWorkoutPlan(),
        apiClient.getDietPlan(),
        apiClient.getProgress()
      ]);

      setWorkoutPlan(workoutResponse.workout_plan);
      setDietPlan(dietResponse.diet_plan);
      setProgressRecords(progressResponse.progress);
    } catch (error: any) {
      toast.error('Failed to load data: ' + error.message);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
  if (progressRecords.length > 0) {
    const allCompleted = progressRecords.flatMap(record => record.completed_workouts);
    setCompletedWorkouts(allCompleted);
  }
}, [progressRecords]);


  // const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  const loadRecommendations = async () => {
    try {
      const res = await apiClient.getRecommendations();
      setRecommendations(res.recommendations);
    } catch (err: any) {
      console.error("Failed to load recommendations", err);
    }
  };
  // const markWorkoutComplete = async (workoutId: string) => {
  //   try {
  //     const newCompleted = [...completedWorkouts, workoutId];
  //     setCompletedWorkouts(newCompleted);
      
  //     await apiClient.submitFeedback({
  //       completed_workouts: newCompleted,
  //       feedback: `Completed workout: ${workoutId}`
  //     });
      
  //     toast.success('Workout marked as complete!');
  //     loadData(); // Refresh progress data
  //   } catch (error: any) {
  //     toast.error('Failed to log workout: ' + error.message);
  //   }
  // };
  const markWorkoutComplete = async (workoutId: string) => {
  try {
    const newCompleted = [...completedWorkouts, workoutId];
    setCompletedWorkouts(newCompleted);

    await apiClient.submitFeedback({
      completed_workouts: newCompleted,
      feedback: `Completed workout: ${workoutId}`
    });

    toast.success('Workout marked as complete!');
  } catch (error: any) {
    toast.error('Failed to log workout: ' + error.message);
  }
};


  const getTodaysWorkout = () => {
    if (!workoutPlan) return null;
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
    return workoutPlan.weekly_schedule.find(day => day.day === today);
  };

  const todaysWorkout = getTodaysWorkout();

  if (loading && !workoutPlan) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p>Loading your personalized plans...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <Dumbbell className="h-8 w-8 text-primary" />
            <h1 className="text-2xl font-bold text-primary">FitLife Dashboard</h1>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <User className="h-4 w-4" />
              <span className="text-sm font-medium">{user?.email}</span>
            </div>
            <Button variant="outline" size="sm" onClick={logout}>
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Welcome Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5" />
              <span>Welcome back, {user?.email?.split('@')[0]}!</span>
            </CardTitle>
            <CardDescription>
              Goal: {user?.fitness_goal} • {user?.workout_days_per_week} days/week • {user?.diet_preference} diet
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary">{user?.weight}kg</div>
                <div className="text-sm text-muted-foreground">Current Weight</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-primary">{user?.height}cm</div>
                <div className="text-sm text-muted-foreground">Height</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-primary">{progressRecords.length}</div>
                <div className="text-sm text-muted-foreground">Logged Sessions</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Today's Workout */}
        {todaysWorkout && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Dumbbell className="h-5 w-5" />
                <span>Today's Workout - {todaysWorkout.focus}</span>
              </CardTitle>
              <CardDescription>
                {workoutPlan?.total_duration} minutes • {workoutPlan?.difficulty_level}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* {todaysWorkout.exercises.map((exercise, index) => ( */}
                {todaysWorkout?.exercises?.map((exercise, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium">{exercise.name}</h4>
                      <p className="text-sm text-muted-foreground">
                        {exercise.sets} sets × {exercise.reps} reps • Rest: {exercise.rest_seconds}s
                      </p>
                    </div>
                    <Button
                      size="sm"
                      onClick={() => markWorkoutComplete(`${todaysWorkout.day}-${exercise.name}`)}
                      disabled={completedWorkouts.includes(`${todaysWorkout.day}-${exercise.name}`)}
                    >
                      {completedWorkouts.includes(`${todaysWorkout.day}-${exercise.name}`) ? 'Completed' : 'Mark Done'}
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        <Tabs defaultValue="workout" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="workout">Workout Plan</TabsTrigger>
            <TabsTrigger value="diet">Diet Plan</TabsTrigger>
            <TabsTrigger value="progress">Progress</TabsTrigger>
            <TabsTrigger value="calendar">Calendar</TabsTrigger>
            <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
          </TabsList>

          <TabsContent value="workout">
            <div className="grid gap-6">
              {/* {workoutPlan?.weekly_schedule.map((day, index) => ( */}
              {workoutPlan?.weekly_schedule?.map((day, index) => (
                <Card key={index}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span>{day.day} - {day.focus}</span>
                      {/* <Badge variant="outline">{day.exercises.length} exercises</Badge> */}
                      <Badge variant="outline">{day.exercises?.length || 0} exercises</Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {/* {day.exercises.map((exercise, exerciseIndex) => ( */}
                      {day.exercises?.map((exercise, exerciseIndex) => (
                        <div key={exerciseIndex} className="flex items-center justify-between p-3 border rounded-lg">
                          <div>
                            <h4 className="font-medium">{exercise.name}</h4>
                            <p className="text-sm text-muted-foreground">
                              {exercise.sets} sets × {exercise.reps} • Rest: {exercise.rest_seconds}s
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}

              {workoutPlan?.safety_tips && (
                <Card>
                  <CardHeader>
                    <CardTitle>Safety Tips</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {/* {workoutPlan.safety_tips.map((tip, index) => ( */}
                      {workoutPlan?.safety_tips?.map((tip, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <span className="text-primary">•</span>
                          <span className="text-sm">{tip}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          <TabsContent value="diet">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Apple className="h-5 w-5" />
                    <span>Daily Nutrition Plan</span>
                  </CardTitle>
                  <CardDescription>
                    {dietPlan?.daily_calories} calories • Tailored for {user?.fitness_goal}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">{dietPlan?.macros.protein}g</div>
                      <div className="text-sm text-muted-foreground">Protein</div>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">{dietPlan?.macros.carbs}g</div>
                      <div className="text-sm text-muted-foreground">Carbs</div>
                    </div>
                    <div className="text-center p-4 bg-orange-50 rounded-lg">
                      <div className="text-2xl font-bold text-orange-600">{dietPlan?.macros.fats}g</div>
                      <div className="text-sm text-muted-foreground">Fats</div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    {/* {dietPlan?.meals.map((meal, index) => ( */}
                    {dietPlan?.meals?.map((meal, index) => (
                      <div key={index} className="p-4 border rounded-lg">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-medium">{meal.meal}</h4>
                          <div className="text-right">
                            <div className="text-sm font-medium">{meal.calories} cal</div>
                            <div className="text-xs text-muted-foreground">{meal.time}</div>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {/* {meal.foods.map((food, foodIndex) => ( */}
                          {meal.foods?.map((food, foodIndex) => (
                            <Badge key={foodIndex} variant="secondary">{food}</Badge>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {dietPlan?.dietary_notes && (
                <Card>
                  <CardHeader>
                    <CardTitle>Nutrition Tips</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {/* {dietPlan.dietary_notes.map((note, index) => ( */}
                      {dietPlan?.dietary_notes?.map((note, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <span className="text-primary">•</span>
                          <span className="text-sm">{note}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          <TabsContent value="progress">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <TrendingUp className="h-5 w-5" />
                  <span>Your Progress</span>
                </CardTitle>
                <CardDescription>Track your fitness journey</CardDescription>
              </CardHeader>
              <CardContent>
                {progressRecords.length > 0 ? (
                  <div className="space-y-4">
                    {progressRecords.slice(0, 10).map((record, index) => (
                      <div key={index} className="p-4 border rounded-lg">
                        <div className="flex justify-between items-start">
                          <div>
                            <div className="font-medium">
                              {new Date(record.created_at).toLocaleDateString()}
                            </div>
                            {record.weight && (
                              <div className="text-sm text-muted-foreground">
                                Weight: {record.weight}kg
                              </div>
                            )}
                            {/* {record.completed_workouts.length > 0 && ( */}
                            {record.completed_workouts?.length > 0 && (
                              <div className="text-sm text-muted-foreground">
                                Completed: {record.completed_workouts.length} exercises
                              </div>
                            )}
                            {record.feedback && (
                              <div className="text-sm text-muted-foreground mt-1">
                                {record.feedback}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <TrendingUp className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">No progress recorded yet. Start working out to see your progress!</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="calendar">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <CalendarIcon className="h-5 w-5" />
                  <span>Workout Schedule</span>
                </CardTitle>
                <CardDescription>Plan and track your workout days</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Calendar
                    mode="single"
                    selected={selectedDate}
                    onSelect={setSelectedDate}
                    className="rounded-md border"
                  />
                  <div className="space-y-4">
                    <h3 className="font-medium">Weekly Schedule</h3>
                    {/* {workoutPlan?.weekly_schedule.map((day, index) => ( */}
                    {workoutPlan?.weekly_schedule?.map((day, index) => (
                      <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <div className="font-medium">{day.day}</div>
                          <div className="text-sm text-muted-foreground">{day.focus}</div>
                        </div>
                        {/* <Badge variant="outline">{day.exercises.length} exercises</Badge> */}
                         <Badge variant="outline">{day.exercises?.length || 0} exercises</Badge>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="recommendations">
            <Card>
              <CardHeader>
                <CardTitle>AI Recommendations</CardTitle>
                <CardDescription>Personalized tips for your workouts and diet</CardDescription>
              </CardHeader>
              <CardContent>
                {recommendations.length === 0 ? (
                  <p className="text-muted-foreground">No recommendations yet. Check back later!</p>
                ) : (
                  <div className="space-y-4">
                    {recommendations.map((rec, idx) => (
                      <div key={idx} className="p-4 border rounded-lg">
                        <div className="font-medium">{rec.title}</div>
                        <div className="text-sm text-muted-foreground">{rec.description}</div>
                        {rec.link && (
                          <a href={rec.link} target="_blank" className="text-blue-600 underline mt-1 block">
                            Learn More
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
      {/* Floating Chatbot */}
      <div className="fixed bottom-5 right-5 z-50 w-80">
        <Chatbot />
      </div>
    </div>
  );
};

export default Dashboard;