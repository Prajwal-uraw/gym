# Project Summary

The FitLife Gym Application is a comprehensive full-stack gym management solution designed to help users achieve their fitness goals through personalized workout and diet plans. Built using modern technologies, it integrates AI to provide tailored recommendations based on user profiles, including dietary preferences and fitness objectives. This application aims to enhance user engagement and progress tracking in fitness routines, making it an essential tool for both gym-goers and fitness coaches.

# Project Module Description

The project consists of two main modules: the backend API and the frontend application.

- **Backend (Python FastAPI + MongoDB)**:

  - User authentication and profile management
  - AI-powered workout and diet plan generation
  - Progress tracking and feedback logging

- **Frontend (React + Tailwind CSS)**:
  - User registration and login interface
  - Dashboard displaying personalized workout and diet plans
  - Progress tracking and feedback submission

# Directory Tree

```
pro/
├── backend/                  # Backend API (FastAPI)
├── dist/                     # Production build output
├── env/                      # Python virtual environment
├── node_modules/             # Node.js dependencies
├── public/                   # Public assets
├── src/                      # Frontend source code
├── .env                      # Environment variables
├── .env.example              # Sample environment variables
├── .gitignore                # Git ignore file
├── components.json           # UI components configuration
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
├── eslint.config.js          # ESLint configuration
├── index.html                # Main HTML file
├── package.json              # Node.js dependencies and scripts
├── pnpm-lock.yaml            # PNPM lockfile
├── postcss.config.js         # PostCSS configuration
├── README.md                 # Project overview and documentation
├── tailwind.config.ts        # Tailwind CSS configuration
├── temp.txt                  # Temporary file
├── template_config.json      # Template configuration
├── tsconfig.app.json         # TypeScript config for app
├── tsconfig.json             # Base TypeScript configuration
├── tsconfig.node.json        # TypeScript config for Node
└── vite.config.ts            # Vite configuration

```

# File Description Inventory

- **DEPLOYMENT_GUIDE.md**: Step-by-step guide for deploying the application.
- **README.md**: Overview and features of the FitLife Gym Application.
- **backend/**: Contains the FastAPI backend code and documentation.
- **components.json**: Configuration file for UI components.
- **eslint.config.js**: Configuration for ESLint to maintain code quality.
- **index.html**: Entry point for the frontend application.
- **package.json**: Manages Node.js dependencies and scripts for the frontend.
- **postcss.config.js**: Configuration for PostCSS processing.
- **public/**: Directory for static assets like images and icons.
- **src/**: Contains the source code for the frontend application, including components, pages, and styles.
- **tailwind.config.ts**: Configuration for Tailwind CSS.
- **template_config.json**: Configuration for UI templates.
- **tsconfig.app.json**: TypeScript configuration specific to the application.
- **tsconfig.json**: Main TypeScript configuration file.
- **vite.config.ts**: Configuration for Vite, the build tool.

# Technology Stack

- **Frontend**:
  - React
  - TypeScript
  - Tailwind CSS
  - Vite
- **Backend**:
  - Python
  - FastAPI
  - MongoDB
  - JWT for authentication
- **AI Integration**: Gemini for personalized recommendations

# Usage

## Installation

1. **Backend**:

   - Navigate to the backend directory:
     ```bash
     cd backend
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up environment variables by copying the example:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file with your MongoDB and JWT secret configurations.

2. **Frontend**:
   - Install dependencies:
     ```bash
     pnpm install
     ```

## Running the Application

1. **Start MongoDB** (if not already running):
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   ```
2. **Run the Backend**:
   ```bash
   python main.py
   ```
3. **Run the Frontend**:
   ```bash
   pnpm run dev
   ```

**Features**:

- AI-generated personalized workout and diet plans tailored to each user's fitness goals and preferences
- AI-powered recommendations to optimize workouts, nutrition, and recovery
- Progress tracking and feedback logging to monitor improvements over time
- Calendar to schedule workouts and track consistency
- Responsive and modern UI built with Tailwind CSS
- JWT-based secure authentication for safe user login and data protection

**Future Improvements**

- Add social sharing features
- Implement video-based workout guidance
- Support multi-language recommendations
- Integrate payment module for premium plans
