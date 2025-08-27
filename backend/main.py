import re
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from motor.motor_asyncio import AsyncIOMotorClient
import openai
import json
from bson import ObjectId
import uvicorn
import ollama
import requests
import pytz
# import google.gen
# erativeai as genai
load_dotenv()
app = FastAPI(title="Gym Management API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"

# MongoDB setup

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = "gym_management"

# OpenAI setup (you'll need to set your API key)
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key")





# Database client
client = None
db = None

@app.on_event("startup")
async def startup_db_client():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()

async def get_db():
    return db
# Pydantic models
class UserSignup(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    password: Optional[str] = None
    age: int
    gender: str
    height: float
    weight: float
    fitness_goal: str
    workout_days_per_week: int
    diet_preference: str
    food_allergies: List[str] = []
    health_conditions: List[str] = []

class UserLogin(BaseModel):
    email: EmailStr
    password: Optional[str] = None

class UserProgress(BaseModel):
    user_id: str
    weight: Optional[float] = None
    completed_workouts: List[str] = []
    feedback: Optional[str] = None
    date: datetime = datetime.now()

class WorkoutPlan(BaseModel):
    exercises: List[Dict[str, Any]]
    total_duration: int
    difficulty_level: str
    focus_areas: List[str]

class DietPlan(BaseModel):
    meals: List[Dict[str, Any]]
    total_calories: int
    macros: Dict[str, float]
    dietary_notes: List[str]

# Utility functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = await db.users.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

#

# def generate_ai_workout_plan(user: dict) -> dict:
#     """Generate AI-powered workout plan based on user profile"""
#     try:
#         DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#         FOCUS_CYCLE = ["Upper Body", "Lower Body", "Full Body & Cardio"]

#         workout_days = min(user.get("workout_days_per_week", 3), 7)
#         weekly_schedule = []

#         for i in range(workout_days):
#             day = DAYS[i]
#             focus = FOCUS_CYCLE[i % len(FOCUS_CYCLE)]

#             if focus == "Upper Body":
#                 exercises = [
#                     {"name": "Push-ups", "sets": 3, "reps": "10-15", "rest_seconds": 60},
#                     {"name": "Pull-ups", "sets": 3, "reps": "5-10", "rest_seconds": 90},
#                     {"name": "Dumbbell Rows", "sets": 3, "reps": "12-15", "rest_seconds": 60},
#                     {"name": "Shoulder Press", "sets": 3, "reps": "10-12", "rest_seconds": 60},
#                 ]
#             elif focus == "Lower Body":
#                 exercises = [
#                     {"name": "Squats", "sets": 3, "reps": "15-20", "rest_seconds": 90},
#                     {"name": "Lunges", "sets": 3, "reps": "12 each leg", "rest_seconds": 60},
#                     {"name": "Deadlifts", "sets": 3, "reps": "10-12", "rest_seconds": 90},
#                     {"name": "Calf Raises", "sets": 3, "reps": "15-20", "rest_seconds": 45},
#                 ]
#             else:  # Full Body & Cardio
#                 exercises = [
#                     {"name": "Burpees", "sets": 3, "reps": "8-12", "rest_seconds": 90},
#                     {"name": "Mountain Climbers", "sets": 3, "reps": "20-30", "rest_seconds": 60},
#                     {"name": "Plank", "sets": 3, "reps": "30-60 seconds", "rest_seconds": 60},
#                     {"name": "Jumping Jacks", "sets": 3, "reps": "30-45", "rest_seconds": 45},
#                 ]

#             weekly_schedule.append({
#                 "day": day,
#                 "focus": focus,
#                 "exercises": exercises
#             })

#         workout_plan = {
#             "weekly_schedule": weekly_schedule,
#             "difficulty_level": "Beginner" if user['age'] > 50 else "Intermediate",
#             "total_duration": 45,
#             "safety_tips": [
#                 "Always warm up before exercising",
#                 "Listen to your body and rest when needed",
#                 "Maintain proper form to prevent injuries",
#                 "Stay hydrated throughout your workout"
#             ]
#         }

#         return workout_plan
#     except Exception as e:
#         return {"error": f"Failed to generate workout plan: {str(e)}"}
    
# import ollama

# import json
import google.generativeai as genai

# Configure your Gemini API key here

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# def generate_ai_workout_plan(user: dict) -> dict:
#     """
#     Generate a frontend-ready workout plan (no extra 'workout_plan' wrapper),
#     ready to send to the frontend.
#     """
#     try:
#         prompt = f"""
#         Generate a personalized workout plan in JSON format ONLY.
#         User profile:
#         - Age: {user.get('age', 30)}
#         - Workout days per week: {user.get('workout_days_per_week', 3)}
#         - Fitness goal: {user.get('goal', 'general fitness')}
#         - Fitness level: {user.get('fitness_level', 'Intermediate')}
#         - Equipment available: {user.get('equipment', 'full gym')}

#         Output JSON must match this structure exactly:
#         {{
#           "weekly_schedule": [...],
#           "difficulty_level": "...",
#           "total_duration": Number,
#           "safety_tips": ["Tip 1", "Tip 2"]
#         }}
#         """

#         model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
#         response = model.generate_content(prompt)
#         generated_text = response.text.strip()

#         # Remove code fences if present
#         if generated_text.startswith("```json"):
#             generated_text = generated_text[7:]
#         if generated_text.endswith("```"):
#             generated_text = generated_text[:-3]
#         generated_text = generated_text.strip()

#         # Load JSON
#         workout_plan = json.loads(generated_text)

#         # Add top-level generated_at
#         # workout_plan["generated_at"] = datetime.utcnow().isoformat()

#         return workout_plan

#     except json.JSONDecodeError as e:
#         raise Exception(f"Failed to parse JSON response from Gemini: {e}")
#     except Exception as e:
#         raise Exception(f"Failed to generate workout plan: {str(e)}")

async def generate_ai_workout_plan(user: dict, db) -> dict:
    """
    Generate a frontend-ready AI workout plan using Gemini and save to MongoDB.
    Returns the saved plan including generated_at.
    """
    try:
        existing_plan = await db.workout_plans.find_one({"user_id": str(user["_id"])})
        if existing_plan:
            return existing_plan.get("workout_plan")
        # Prepare prompt for Gemini
        prompt = f"""
        Generate a personalized workout plan in JSON format ONLY.
        User profile:
        - Age: {user.get('age', 30)}
        - Workout days per week: {user.get('workout_days_per_week', 3)}
        - Fitness goal: {user.get('fitness_goal', 'general fitness')}
        - Fitness level: {user.get('fitness_level', 'Intermediate')}
        - Equipment available: {user.get('equipment', 'full gym')}

        Output JSON must match this structure exactly:
        {{
          "weekly_schedule": [...],
          "difficulty_level": "...",
          "total_duration": Number,
          "safety_tips": ["Tip 1", "Tip 2"]
        }}
        """

        # Call Gemini
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
        response = model.generate_content(prompt)
        generated_text = response.text.strip()

        # Remove code fences if any
        if generated_text.startswith("```json"):
            generated_text = generated_text[7:]
        if generated_text.endswith("```"):
            generated_text = generated_text[:-3]
        generated_text = generated_text.strip()

        # Load JSON
        workout_plan = json.loads(generated_text)

        # Add generated timestamp
        # workout_plan["generated_at"] = datetime.utcnow()

        # Save to MongoDB (upsert: update if exists, insert if new)
        await db.workout_plans.update_one(
            {"user_id": str(user["_id"])},
            {"$set": {"user_id": str(user["_id"]), "workout_plan": workout_plan}},
            upsert=True
        )

        return workout_plan

    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response from Gemini: {e}")
    except Exception as e:
        raise Exception(f"Failed to generate or save workout plan: {str(e)}")

#

# def generate_ai_diet_plan(user: dict) -> dict:
#     """Generate AI-powered diet plan based on user profile"""
#     try:
#         # Calculate BMR and daily calorie needs
#         if user['gender'].lower() == 'male':
#             bmr = 88.362 + (13.397 * user['weight']) + (4.799 * user['height']) - (5.677 * user['age'])
#         else:
#             bmr = 447.593 + (9.247 * user['weight']) + (3.098 * user['height']) - (4.330 * user['age'])
        
#         activity_multiplier = 1.375 + (user['workout_days_per_week'] * 0.075)
#         daily_calories = int(bmr * activity_multiplier)
        
#         # Adjust calories based on fitness goal
#         if user['fitness_goal'].lower() == 'fat loss':
#             daily_calories = int(daily_calories * 0.85)
#         elif user['fitness_goal'].lower() == 'muscle gain':
#             daily_calories = int(daily_calories * 1.15)
        
#         diet_plan = {
#             "daily_calories": daily_calories,
#             "meals": [
#                 {
#                     "meal": "Breakfast",
#                     "foods": ["Oatmeal with berries", "Greek yogurt", "Green tea"],
#                     "calories": int(daily_calories * 0.25),
#                     "time": "7:00 AM"
#                 },
#                 {
#                     "meal": "Lunch",
#                     "foods": ["Grilled chicken breast", "Brown rice", "Mixed vegetables"],
#                     "calories": int(daily_calories * 0.35),
#                     "time": "12:30 PM"
#                 },
#                 {
#                     "meal": "Snack",
#                     "foods": ["Apple with almonds", "Protein shake"],
#                     "calories": int(daily_calories * 0.15),
#                     "time": "3:30 PM"
#                 },
#                 {
#                     "meal": "Dinner",
#                     "foods": ["Salmon fillet", "Quinoa", "Steamed broccoli"],
#                     "calories": int(daily_calories * 0.25),
#                     "time": "7:00 PM"
#                 }
#             ],
#             "macros": {
#                 "protein": int(daily_calories * 0.25 / 4),
#                 "carbs": int(daily_calories * 0.45 / 4),
#                 "fats": int(daily_calories * 0.30 / 9)
#             },
#             "dietary_notes": [
#                 "Drink at least 8 glasses of water daily",
#                 "Avoid processed foods",
#                 "Include variety in your meals",
#                 "Eat slowly and mindfully"
#             ]
#         }
        
#         # Adjust for dietary preferences
#         if user['diet_preference'].lower() == 'vegetarian':
#             diet_plan['meals'][1]['foods'] = ["Lentil curry", "Brown rice", "Mixed vegetables"]
#             diet_plan['meals'][3]['foods'] = ["Tofu stir-fry", "Quinoa", "Steamed broccoli"]
        
#         return diet_plan
#     except Exception as e:
#         return {"error": f"Failed to generate diet plan: {str(e)}"}

async def generate_ai_diet_plan(user: dict,db) -> dict:
    """
    Generate a frontend-ready AI diet plan based on user profile using Gemini.
    Output matches frontend-ready structure directly:
    {
        "daily_calories": Number,
        "meals": [...],
        "macros": {...},
        "dietary_notes": [...]
    }
    """
    try:
        # Prepare prompt for Gemini
        prompt = f"""
        Generate a personalized diet plan in JSON format ONLY.
        User profile:
        - Age: {user.get('age', 30)}
        - Gender: {user.get('gender', 'male')}
        - Weight (kg): {user.get('weight', 70)}
        - Height (cm): {user.get('height', 170)}
        - Workout days per week: {user.get('workout_days_per_week', 3)}
        - Fitness goal: {user.get('fitness_goal', 'general fitness')}
        - Diet preference: {user.get('diet_preference', 'none')}

        Output JSON must match this structure exactly:
        {{
          "daily_calories": Number,
          "meals": [
            {{
              "meal": "...",
              "foods": ["..."],
              "calories": Number,
              "time": "..."
            }}
          ],
          "macros": {{
            "protein": Number,
            "carbs": Number,
            "fats": Number
          }},
          "dietary_notes": ["Tip 1", "Tip 2"]
        }}
        """

        # Call Gemini
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
        response = model.generate_content(prompt)
        generated_text = response.text.strip()

        # Remove code fences if present
        if generated_text.startswith("```json"):
            generated_text = generated_text[7:]
        if generated_text.endswith("```"):
            generated_text = generated_text[:-3]
        generated_text = generated_text.strip()

        # Load JSON
        diet_plan = json.loads(generated_text)

        # Optional: add timestamp if frontend needs
        # diet_plan["generated_at"] = datetime.utcnow().isoformat()
        await db.workout_plans.update_one(
            {"user_id": str(user["_id"])},
            {"$set": {"user_id": str(user["_id"]), "diet_plan": diet_plan}},
            upsert=True
        )

        return diet_plan

    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response from Gemini: {e}")
    except Exception as e:
        raise Exception(f"Failed to generate diet plan: {str(e)}")


#   working  
# def generate_ai_diet_plan(user: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Generate AI-powered diet plan based on user profile using Gemini API.
#         Returns a structured dict with daily_calories, meals, macros, and dietary_notes.
#         """

#         url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
#         headers = {
#             "Content-Type": "application/json",
#             "X-goog-api-key": GEMINI_API_KEY,
#         }

#         prompt = f"""
#         Create a personalized {user.get('workout_days_per_week', 3)}-day diet plan.

#         User profile:
#         - Age: {user.get('age')}
#         - Gender: {user.get('gender')}
#         - Weight: {user.get('weight')} kg
#         - Height: {user.get('height')} cm
#         - Fitness Goal: {user.get('goal')}
#         - Diet Preference: {user.get('diet_preference', 'balanced')}
#         - Workout Days per Week: {user.get('workout_days_per_week', 3)}

#         Respond ONLY in valid JSON format with keys:
#         - daily_calories
#         - meals (list of meals with foods, calories, and time)
#         - macros (protein, carbs, fats)
#         - dietary_notes
#         """

#         payload = {"contents": [{"parts": [{"text": prompt}]}]}

#         try:
#             response = requests.post(url, headers=headers, json=payload, timeout=30)
#             response_json = response.json()

#             # Extract AI text response
#             text = ""
#             if "candidates" in response_json:
#                 candidate = response_json["candidates"][0]
#                 if "content" in candidate and "parts" in candidate["content"]:
#                     text = candidate["content"]["parts"][0].get("text", "")

#             if not text:
#                 return {"error": "No response from Gemini API", "raw_response": response_json}

#             # Clean ```json wrappers if present
#             text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
#             text = re.sub(r"\s*```$", "", text.strip())

#             # Parse JSON safely
#             try:
#                 return json.loads(text)
#             except json.JSONDecodeError:
#                 return {"plan_text": text, "raw_response": response_json}

#         except Exception as e:
#             return {"error": str(e)}


# def generate_ai_diet_plan(user: dict) -> dict:
#     """Generate AI-powered diet plan based on user profile using Gemini API"""
#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
#     headers = {
#         "Content-Type": "application/json",
#         "X-goog-api-key": GEMINI_API_KEY
#     }

#     prompt = f"""
#     Create a personalized {user.get('workout_days_per_week', 3)}-day **diet plan**.

#     User profile:
#     - Age: {user.get('age')}
#     - Gender: {user.get('gender')}
#     - Weight: {user.get('weight')} kg
#     - Height: {user.get('height')} cm
#     - Fitness Goal: {user.get('goal')}
#     - Diet Preference: {user.get('diet_preference', 'balanced')}
#     - Workout Days per Week: {user.get('workout_days_per_week', 3)}

#     Respond ONLY in valid JSON format with keys:
#     - daily_calories
#     - meals (list of meals with foods, calories, and time)
#     - macros (protein, carbs, fats)
#     - dietary_notes
#     """

#     payload = {"contents": [{"parts": [{"text": prompt}]}]}

#     try:
#         response = requests.post(url, headers=headers, json=payload).json()

#         # Extract AI text response
#         text = ""
#         if response.get("candidates"):
#             candidate = response["candidates"][0]
#             if candidate.get("content") and "parts" in candidate["content"]:
#                 text = candidate["content"]["parts"][0].get("text", "")

#         if not text:
#             return {"error": "No response from Gemini API", "raw_response": response}

#         # Remove ```json markers if present
#         text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
#         text = re.sub(r"\s*```$", "", text.strip())

#         # Parse JSON
#         try:
#             return json.loads(text)
#         except json.JSONDecodeError:
#             return {"plan_text": text}

#     except Exception as e:
#         return {"error": str(e)}
# API Endpoints
@app.post("/signup")
async def signup(user_data: UserSignup):
    try:
        # Check if user exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password if provided
        hashed_password = None
        if user_data.password:
            hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user document
        user_doc = {
            **user_data.dict(),
            "password": hashed_password,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Insert user
        result = await db.users.insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        # Generate token
        access_token = create_access_token(
            data={"sub": user_data.email, "user_id": user_id},
            expires_delta=timedelta(days=30)
        )
        
        return {
            "message": "User created successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
async def login(user_credentials: UserLogin):
    try:
        user = await db.users.find_one({"email": user_credentials.email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Check password if provided
        if user_credentials.password and user.get("password"):
            if not bcrypt.checkpw(user_credentials.password.encode('utf-8'), user["password"]):
                raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate token
        access_token = create_access_token(
            data={"sub": user["email"], "user_id": str(user["_id"])},
            expires_delta=timedelta(days=30)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": str(user["_id"]),
            "message": "Login successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# def fix_mongo_object_ids(data):
#     if isinstance(data, dict):
#         return {k: fix_mongo_object_ids(v) for k, v in data.items()}
#     elif isinstance(data, list):
#         return [fix_mongo_object_ids(i) for i in data]
#     elif isinstance(data, ObjectId):
#         return str(data)
#     else:
#         return data

# @app.post("/login")
# async def login(user_credentials: UserLogin):
#     try:
#         # Find user by email
#         user = await db.users.find_one({"email": user_credentials.email})
#         if not user:
#             raise HTTPException(status_code=401, detail="Invalid credentials")
        
#         # Check password if provided
#         if user_credentials.password and user.get("password"):
#             if not bcrypt.checkpw(user_credentials.password.encode('utf-8'), user["password"]):
#                 raise HTTPException(status_code=401, detail="Invalid credentials")
        
#         # Generate JWT token
#         access_token = create_access_token(
#             data={"sub": user["email"], "user_id": str(user["_id"])},
#             expires_delta=timedelta(days=30)
#         )

#         # Fetch user's plans and progress
#         workout_plan_doc = await db.workout_plans.find_one({"user_id": str(user["_id"])})
#         diet_plan_doc = await db.diet_plans.find_one({"user_id": str(user["_id"])})
#         progress_doc = await db.progress.find_one({"user_id": str(user["_id"])})

#         # Convert ObjectId to string for JSON serialization
#         workout_plan = fix_mongo_object_ids(workout_plan_doc.get("workout_plan")) if workout_plan_doc else None
#         diet_plan = fix_mongo_object_ids(diet_plan_doc.get("diet_plan")) if diet_plan_doc else None
#         progress = fix_mongo_object_ids(progress_doc.get("progress")) if progress_doc else None

#         # Return response
#         return {
#             "access_token": access_token,
#             "token_type": "bearer",
#             "user_id": str(user["_id"]),
#             "user": fix_mongo_object_ids(user),
#             "workout_plan": workout_plan,
#             "diet_plan": diet_plan,
#             "progress": progress,
#             "message": "Login successful"
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

    
@app.get("/workout-plan")
async def get_workout_plan(current_user: dict = Depends(get_current_user)):
    try:
        workout_plan =  await generate_ai_workout_plan(current_user, db)
        nepal_tz = pytz.timezone("Asia/Kathmandu")
        nepal_time = datetime.now(nepal_tz)
        return {"workout_plan": workout_plan, "generated_at": nepal_time.isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# @app.get("/workout-plan")
# async def get_workout_plan(current_user: dict = Depends(get_current_user)):
#     try:
#         # Generate AI workout plan
#         workout_plan = generate_ai_workout_plan(current_user)
        
#         # Add timestamp
#         workout_plan["generated_at"] = datetime.utcnow().isoformat()
        
#         # Save to MongoDB
#         await db.workout_plans.update_one(
#             {"user_id": str(current_user["_id"])},
#             {"$set": workout_plan},
#             upsert=True  # create if not exists
#         )
        
#         return {"workout_plan": workout_plan}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/diet-plan")
async def get_diet_plan(current_user: dict = Depends(get_current_user)):
    try:
        diet_plan = await generate_ai_diet_plan(current_user, db)
        return {"diet_plan": diet_plan, "generated_at": datetime.now()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# @app.get("/diet-plan")
# async def get_diet_plan(current_user: dict = Depends(get_current_user)):
#     try:
#         # Generate AI diet plan
#         diet_plan = generate_ai_diet_plan(current_user)
        
#         # Add timestamp
#         diet_plan["generated_at"] = datetime.utcnow().isoformat()
        
#         # Save to MongoDB
#         await db.diet_plans.update_one(
#             {"user_id": str(current_user["_id"])},
#             {"$set": diet_plan},
#             upsert=True
#         )
        
#         # Return wrapped for frontend
#         return {"diet_plan": diet_plan}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def submit_feedback(progress: UserProgress, current_user: dict = Depends(get_current_user)):
    try:
        progress_doc = {
            **progress.dict(),
            "user_id": str(current_user["_id"]),
            "created_at": datetime.now()
        }
        
        result = await db.progress.insert_one(progress_doc)
        
        return {
            "message": "Progress logged successfully",
            "progress_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    try:
        # Remove sensitive information
        profile = {k: v for k, v in current_user.items() if k not in ["password", "_id"]}
        profile["user_id"] = str(current_user["_id"])
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress")
async def get_progress(current_user: dict = Depends(get_current_user)):
    try:
        progress_records = []
        async for record in db.progress.find({"user_id": str(current_user["_id"])}):
            record["_id"] = str(record["_id"])
            progress_records.append(record)
        
        return {"progress": progress_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Gym Management API is running!", "version": "1.0.0"}
# from pydantic import BaseModel

class ChatQuery(BaseModel):
    message: str

@app.post("/chatbot")
async def chatbot(query: ChatQuery, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    msg = query.message.lower().strip()

    # Handle generic greetings
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if msg in greetings:
        return {"reply": f"Hello! How can I help you with your fitness today?"}
    
    user_id = str(current_user["_id"])

    # Fetch user data
    workout_plan = await db.workout_plans.find_one({"user_id": user_id})
    diet_plan = await db.diet_plans.find_one({"user_id": user_id})
    progress = await db.progress.find_one({"user_id": user_id})

    # Combine into context
    context = {
        "workout_plan": workout_plan.get("workout_plan") if workout_plan else None,
        "diet_plan": diet_plan.get("diet_plan") if diet_plan else None,
        "progress": progress.get("progress") if progress else None
    }

    prompt = f"""
        You are a friendly fitness assistant chatbot. Always try to answer the user based on their personal fitness data if available.

        User Query: {query.message}

        User Data:
        {json.dumps(context, indent=2)}

        Rules:
        - If the user asks something related to their workout, diet, or progress, answer using their data.
        - If the user asks a greeting, thanks, or any small talk, respond naturally and politely.
        - If the information is not in the user's data, give a helpful or friendly answer instead of saying you don't know.
        - Respond naturally to greetings or small talk.
        - Provide clear advice and format your answer with newlines and bullets.
        """

    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    response = model.generate_content(prompt)

    return {"reply": response.text.strip()}

# @app.post("/chatbot")
# async def chatbot(
#     query: ChatQuery,
#     current_user: dict = Depends(get_current_user),
#     db=Depends(get_db)
# ):
#     msg = query.message.lower().strip()
#     greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    
#     if msg in greetings:
#         return {"reply": "Hello! How can I help you with your fitness today?"}

#     user_id = str(current_user["_id"])

#     # Fetch user data
#     workout_plan = await db.workout_plans.find_one({"user_id": user_id})
#     diet_plan = await db.diet_plans.find_one({"user_id": user_id})
#     progress = await db.progress.find_one({"user_id": user_id})

#     # Format user data safely
#     def format_user_data(data: dict) -> str:
#         lines = []
#         for key, value in data.items():
#             if isinstance(value, list):
#                 lines.append(f"{key}:")
#                 if value:
#                     for item in value:
#                         lines.append(f"  - {json.dumps(item)}")
#                 else:
#                     lines.append("  No data available")
#             else:
#                 lines.append(f"{key}: {value if value else 'No data available'}")
#         return "\n".join(lines)

#     context = {
#         "workout_plan": workout_plan.get("workout_plan") if workout_plan else None,
#         "diet_plan": diet_plan.get("diet_plan") if diet_plan else None,
#         "progress": progress.get("progress") if progress else None
#     }

#     context_text = format_user_data(context)

#     prompt = f"""
# You are a friendly fitness assistant chatbot.

# User Query: {query.message}

# User Data:
# {context_text}

# Rules:
# - Answer based on user's data if possible.
# - Respond naturally to greetings or small talk.
# - Provide clear advice and format your answer with newlines and bullets.
# """

#     model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    
#     try:
#         response = await model.generate_content(prompt)
#         reply = response.text.strip()
#         # Fallback formatting
#         if not reply:
#             reply = "Sorry, I couldn't generate a response at the moment."
#     except Exception as e:
#         print("Gemini error:", e)
#         reply = "Sorry, I couldn't generate a response at the moment."

#     return {"reply": reply}

@app.post("/recommendations")
async def get_recommendations(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    user_id = str(current_user["_id"])

    # Fetch user data
    workout_plan = await db.workout_plans.find_one({"user_id": user_id})
    diet_plan = await db.diet_plans.find_one({"user_id": user_id})
    progress = await db.progress.find_one({"user_id": user_id})

    context = {
        "workout_plan": workout_plan.get("workout_plan") if workout_plan else None,
        "diet_plan": diet_plan.get("diet_plan") if diet_plan else None,
        "progress": progress.get("progress") if progress else None
    }

    context_text = json.dumps(context, indent=2)

    prompt = f"""
You are a friendly fitness assistant. Provide 3 personalized recommendations for the user.

Include:
- Exercise video links or descriptions
- Diet/meal suggestions or links
- Motivational or recovery tips

User Data:
{context_text}

Respond ONLY in a JSON array of 3 items. Each item should be:
{{
    "type": "exercise|diet|tip",
    "title": "Short title",
    "description": "Detailed description",
    "link": "Optional URL"
}}

Do NOT include any text outside the JSON array.
"""

    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

    try:
        response = model.generate_content(prompt)  # synchronous call
        raw_text = response.text.strip()
        print("AI raw response:", raw_text)

        # Clean any ```json ... ``` formatting
        import re
        cleaned_text = re.sub(r"^```(?:json)?|```$", "", raw_text, flags=re.MULTILINE).strip()

        # Parse JSON
        try:
            recommendations = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            print("JSON parsing error:", str(e))
            recommendations = []

    except Exception as e:
        print("AI generation error:", str(e))
        recommendations = []

    # Ensure fallback of 3 items
    while len(recommendations) < 3:
        recommendations.append({
            "type": "tip",
            "title": "General Tip",
            "description": "Stay active and hydrated!",
            "link": ""
        })

    return {"recommendations": recommendations}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


