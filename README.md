# AI Code Reviewer

An intelligent code review assistant that uses AI to analyze pull requests, detect potential issues, and suggest improvements. The system leverages multiple AI models to provide comprehensive code analysis.

## Features

- 🤖 AI-powered code analysis
- 🔒 Security vulnerability detection
- 🚀 Performance optimization suggestions
- ✨ Code style recommendations
- 🔄 Real-time progress tracking

## Prerequisites

Before you begin, ensure you have installed:
- Python 3.8+
- Node.js 16+
- Redis
- Git

You'll also need:
- GitHub Account and Personal Access Token
- OpenAI API Key

## Quick Start

1. **Clone and Setup Project Structure**
   ```bash
   # Clone repository and create directories
   git clone https://github.com/yourusername/ai-code-reviewer.git
   cd ai-code-reviewer
   mkdir backend frontend tests
   ```

2. **Backend Setup**
   ```bash
   # Setup Python environment
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend

   # Install dependencies including required type definitions
   npm install
   npm install --save-dev @types/react @types/node @types/axios @types/react-dom
   ```

4. **Environment Configuration**

   Create `backend/.env`:
   ```env
   GITHUB_TOKEN=your_github_token
   OPENAI_API_KEY=your_openai_key
   SECRET_KEY=your_jwt_secret_key
   REDIS_URL=redis://localhost:6379
   ```

   Create `frontend/.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## Running the Application

1. **Start Redis**
   ```bash
   redis-server
   ```

2. **Start Backend Services**
   ```bash
   # Terminal 1: Start Celery Worker
   cd backend
   celery -A celery_worker worker --loglevel=info

   # Terminal 2: Start FastAPI Server
   cd backend
   uvicorn app:app --reload
   ```

3. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

Access the application:
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## Fixing Common TypeScript Errors

If you encounter TypeScript errors:

1. **React Module Not Found**
   ```bash
   npm install --save-dev @types/react @types/react-dom
   ```

2. **Axios Module Not Found**
   ```bash
   npm install --save-dev @types/axios
   ```

3. **Add TypeScript Configuration**

   Create or update `frontend/tsconfig.json`:
   ```json
   {
     "compilerOptions": {
       "target": "es5",
       "lib": ["dom", "dom.iterable", "esnext"],
       "allowJs": true,
       "skipLibCheck": true,
       "strict": true,
       "forceConsistentCasingInFileNames": true,
       "noEmit": true,
       "esModuleInterop": true,
       "module": "esnext",
       "moduleResolution": "node",
       "resolveJsonModule": true,
       "isolatedModules": true,
       "jsx": "preserve",
       "incremental": true
     },
     "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
     "exclude": ["node_modules"]
   }
   ```

## Project Structure
