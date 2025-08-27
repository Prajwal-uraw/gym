# FitLife Gym Backend API

A comprehensive gym management backend built with FastAPI, featuring AI-powered workout and diet plan generation.

## Features

- 🔐 **User Authentication**: JWT-based authentication with optional password
- 👤 **User Profiles**: Comprehensive health and fitness profile management
- 🤖 **AI Integration**: Personalized workout and diet plans using AI algorithms
- 📊 **Progress Tracking**: Log and monitor fitness progress over time
- 🏋️ **Workout Plans**: Dynamic exercise routines based on user goals
- 🍎 **Diet Plans**: Customized nutrition plans with macro tracking
- 💬 AI Chatbot: Context-aware chatbot for fitness guidance
- 📱 **RESTful API**: Clean, documented API endpoints
- ✅ Recommendations: Personalized fitness and dietary suggestions based on progress

## Quick Start

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud instance)
- Google API Key (for Gemini AI features)

### Installation

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:

   ```
   MONGODB_URL=mongodb://localhost:27017
   SECRET_KEY=your-super-secret-jwt-key-here
   OPENAI_API_KEY=your-openai-api-key-here  # Optional
   ```

3. **Start MongoDB:**

   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest

   # Or install MongoDB locally
   # https://docs.mongodb.com/manual/installation/
   ```

4. **Run the server:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /signup` - Create new user account
- `POST /login` - User authentication

### User Management

- `GET /profile` - Get user profile
- `GET /progress` - Get user progress history

### AI Features

- `GET /workout-plan` - Get personalized workout plan
- `GET /diet-plan` - Get personalized diet plan
- `POST /feedback` - Submit progress feedback
- `POST /chatbot` - Ask fitness questions; AI responds using user-specific data
- `GET /recommendations` - Get personalized fitness and dietary recommendations

### Health Check

- `GET /` - API status

## API Documentation

Once the server is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### 1. Create Account

```bash
curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "age": 25,
    "gender": "male",
    "height": 180,
    "weight": 75,
    "fitness_goal": "muscle gain",
    "workout_days_per_week": 4,
    "diet_preference": "balanced",
    "food_allergies": [],
    "health_conditions": []
  }'
```

### 2. Get Workout Plan

```bash
curl -X GET "http://localhost:8000/workout-plan" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Log Progress

```bash
curl -X POST "http://localhost:8000/feedback" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "weight": 74.5,
    "completed_workouts": ["Monday-Push-ups", "Monday-Pull-ups"],
    "feedback": "Great workout today!"
  }'
```

## AI Features

The backend includes intelligent algorithms for:

### Workout Plan Generation

- Exercises tailored to fitness goals
- Appropriate sets, reps, and rest periods
- Progressive difficulty adjustment
- Safety considerations for health conditions

### Diet Plan Generation

- Calorie calculation based on BMR and activity level
- Macro distribution optimization
- Dietary restriction compliance
- Meal timing recommendations

### Progress Analysis

- Performance trend analysis
- Plan adjustment recommendations
- Motivational insights

### AI Chatbot

- Responds based on the user’s workout, diet, and progress data
- Friendly, natural language replies
- Provides tips, suggestions, and

### Recommendations

- Personalized guidance based on workout and diet progress
- Suggestions to optimize workouts (e.g., increase reps, add cardio, rest days)
- Dietary tips based on calories, macros, and preferences
- Safety alerts and health reminders
- Encouragement and motivation to maintain consistency

## Database Schema

### Users Collection

```javascript
{
  _id: ObjectId,
  email: String,
  phone: String,
  password: String (hashed),
  age: Number,
  gender: String,
  height: Number,
  weight: Number,
  fitness_goal: String,
  workout_days_per_week: Number,
  diet_preference: String,
  food_allergies: [String],
  health_conditions: [String],
  created_at: Date,
  updated_at: Date
}
```

### Progress Collection

```javascript
{
  _id: ObjectId,
  user_id: String,
  weight: Number,
  completed_workouts: [String],
  feedback: String,
  date: Date,
  created_at: Date
}
```

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Pydantic
- Rate limiting ready (can be added)

## Deployment

### Production Setup

1. **Environment Variables:**

   ```bash
   export MONGODB_URL="mongodb://production-server:27017"
   export SECRET_KEY="your-production-secret-key"
   export OPENAI_API_KEY="your-openai-key"
   ```

2. **Production Server:**
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
