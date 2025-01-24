from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class SecurityRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CodeIssue(BaseModel):
    file_path: str
    line_number: int
    issue_type: str
    description: str
    suggestion: str
    risk_level: SecurityRisk

class ReviewRequest(BaseModel):
    repository: str
    pull_request_number: int
    analysis_depth: Optional[str] = "standard"

class ReviewResponse(BaseModel):
    task_id: str

class CodeAnalysis(BaseModel):
    status: str
    completion_percentage: float
    issues: Optional[List[CodeIssue]] = None
    summary: Optional[str] = None
    estimated_review_time: Optional[int] = None 