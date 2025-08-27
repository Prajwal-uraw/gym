# 🚀 FitLife Gym - Complete Deployment Guide

This guide provides step-by-step instructions to deploy both the frontend and backend of the FitLife Gym application.

## 📋 Prerequisites

### Backend Requirements
- Python 3.8 or higher
- MongoDB (local installation or cloud service like MongoDB Atlas)
- Git

### Frontend Requirements  
- Node.js 18 or higher
- pnpm (recommended) or npm

## 🔧 Backend Deployment

### Step 1: Set Up MongoDB

#### Option A: Local MongoDB Installation
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install -y mongodb

# On macOS with Homebrew
brew tap mongodb/brew
brew install mongodb-community

# On Windows
# Download from https://www.mongodb.com/try/download/community
```

#### Option B: MongoDB Atlas (Cloud)
1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a new cluster
4. Get your connection string (format: `mongodb+srv://username:password@cluster.mongodb.net/database`)

### Step 2: Backend Setup

```bash
# Clone and navigate to project
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

### Step 3: Configure Environment Variables

Edit the `.env` file:

```bash
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017  # or your MongoDB Atlas connection string

# JWT Secret (generate a secure random key)
SECRET_KEY=your-super-secret-jwt-key-generate-a-random-string-here

# OpenAI API Key (optional - for enhanced AI features)
OPENAI_API_KEY=your-openai-api-key-here

# Environment
ENVIRONMENT=production
```

**🔐 Security Note**: Generate a strong SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Start Backend Server

#### Development Mode
```bash
python main.py
```

#### Production Mode with Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The backend will be available at `http://localhost:8000`

### Step 5: Verify Backend
Visit `http://localhost:8000/docs` to see the interactive API documentation.

## 🎨 Frontend Deployment

### Step 1: Install Dependencies

```bash
# Install pnpm if you don't have it
npm install -g pnpm

# Install project dependencies
pnpm install
```

### Step 2: Configure API Endpoint

If your backend is running on a different host/port, update the API base URL in `src/lib/api.ts`:

```typescript
const API_BASE_URL = 'http://your-backend-host:8000';
```

### Step 3: Build and Run Frontend

#### Development Mode
```bash
pnpm run dev
```
The frontend will be available at `http://localhost:5173`

#### Production Build
```bash
# Build for production
pnpm run build

# Preview production build locally
pnpm run preview
```

#### Serve Production Build
```bash
# Install a static file server
npm install -g serve

# Serve the built files
serve -s dist -l 3000
```

## 🌐 Production Deployment Options

### Option 1: Traditional VPS/Server

#### Backend (FastAPI)
```bash
# Use systemd service (Linux)
sudo nano /etc/systemd/system/fitlife-backend.service
```

Service file content:
```ini
[Unit]
Description=FitLife Gym Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/your/backend
Environment=PATH=/path/to/your/backend/venv/bin
ExecStart=/path/to/your/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start the service
sudo systemctl enable fitlife-backend
sudo systemctl start fitlife-backend
```

#### Frontend (React)
Serve the built files using Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/your/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY . .
RUN pnpm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: fitlife-mongo
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  backend:
    build: ./backend
    container_name: fitlife-backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - SECRET_KEY=your-secret-key
    depends_on:
      - mongodb

  frontend:
    build: .
    container_name: fitlife-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mongodb_data:
```

### Option 3: Cloud Deployment

#### Vercel (Frontend)
1. Push your code to GitHub
2. Connect your GitHub repo to Vercel
3. Set build command: `pnpm run build`
4. Set output directory: `dist`
5. Deploy!

#### Railway (Backend)
1. Push your backend code to GitHub
2. Connect to Railway
3. Add environment variables
4. Deploy automatically

#### Heroku (Full Stack)
```bash
# Install Heroku CLI
# Create Procfile for backend
echo "web: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:\$PORT" > Procfile

# Deploy to Heroku
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
heroku config:set MONGODB_URL=your-mongodb-atlas-url
git push heroku main
```

## 🔧 Environment-Specific Configuration

### Development
- Use local MongoDB
- Enable debug logging
- CORS allows localhost

### Staging  
- Use MongoDB Atlas
- Reduced logging
- Limited CORS origins

### Production
- Use MongoDB Atlas with replica sets
- Minimal logging
- Strict CORS policy
- Enable rate limiting
- Use HTTPS only
- Environment variable validation

## 📊 Monitoring & Maintenance

### Health Checks
- Backend: `GET /` endpoint
- Database: Monitor MongoDB connection
- Frontend: Check if assets load correctly

### Logs
```bash
# Backend logs
tail -f /var/log/fitlife-backend.log

# System logs
journalctl -u fitlife-backend -f
```

### Database Backup
```bash
# MongoDB backup
mongodump --host localhost:27017 --db gym_management --out /backup/
```

## 🚨 Troubleshooting

### Common Issues

1. **Backend won't start**
   - Check MongoDB connection
   - Verify environment variables
   - Check port availability

2. **Frontend API calls fail**
   - Verify backend is running
   - Check CORS configuration
   - Confirm API base URL

3. **Database connection issues**
   - MongoDB service status
   - Network connectivity
   - Authentication credentials

4. **Build failures**
   - Node.js version compatibility
   - Clear node_modules and reinstall
   - Check for TypeScript errors

### Performance Optimization

1. **Backend**
   - Use connection pooling
   - Enable response compression
   - Implement caching
   - Add database indexes

2. **Frontend**
   - Code splitting
   - Image optimization
   - Bundle analysis
   - CDN for static assets

## 🔐 Security Checklist

- [ ] Strong JWT secret key
- [ ] Environment variables secured
- [ ] HTTPS enabled in production
- [ ] CORS properly configured
- [ ] Database access restricted
- [ ] Input validation enabled
- [ ] Rate limiting implemented
- [ ] Security headers configured

## 📞 Support

For issues or questions:
1. Check the logs first
2. Verify configuration
3. Test with minimal setup
4. Check GitHub issues
5. Create detailed bug reports

---

**🎉 Congratulations!** Your FitLife Gym application should now be running successfully!