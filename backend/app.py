from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
import github3
from models import ReviewRequest, ReviewResponse, CodeAnalysis
from services.github_service import GitHubService
from services.ai_service import AICodeReviewService
from services.auth_service import AuthService
from celery_worker import process_review

app = FastAPI(title="AI Code Reviewer")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_service = AuthService()
github_service = GitHubService()
ai_service = AICodeReviewService()

@app.post("/api/review", response_model=ReviewResponse)
async def create_review(
    request: ReviewRequest,
    token: str = Depends(oauth2_scheme)
):
    user = auth_service.verify_token(token)
    
    # Validate repository access
    if not github_service.has_repo_access(user, request.repository):
        raise HTTPException(status_code=403, detail="Repository access denied")
    
    # Create async task for processing
    task = process_review.delay(
        repo_url=request.repository,
        pull_request_number=request.pull_request_number,
        user_id=user.id
    )
    
    return ReviewResponse(task_id=task.id)

@app.get("/api/review/{task_id}", response_model=CodeAnalysis)
async def get_review_status(
    task_id: str,
    token: str = Depends(oauth2_scheme)
):
    user = auth_service.verify_token(token)
    result = process_review.AsyncResult(task_id)
    
    if result.ready():
        return result.get()
    else:
        return CodeAnalysis(
            status="processing",
            completion_percentage=result.info.get('progress', 0)
        )

@app.post("/api/token")
async def login(username: str, password: str):
    user = auth_service.authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth_service.create_token(user)
    return {"access_token": access_token, "token_type": "bearer"} 