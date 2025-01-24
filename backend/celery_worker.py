from celery import Celery
from services.github_service import GitHubService
from services.ai_service import AICodeReviewService
from models import CodeAnalysis

celery_app = Celery(
    'ai_code_reviewer',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

@celery_app.task(bind=True)
def process_review(self, repo_url: str, pull_request_number: int, user_id: str):
    github_service = GitHubService()
    ai_service = AICodeReviewService()
    
    # Update task status
    self.update_state(
        state='PROGRESS',
        meta={'progress': 0}
    )
    
    # Get PR details
    pr_details = github_service.get_pull_request(repo_url, pull_request_number)
    
    # Update progress
    self.update_state(
        state='PROGRESS',
        meta={'progress': 20}
    )
    
    # Get diff and context
    diff = github_service.get_pr_diff(repo_url, pull_request_number)
    context = github_service.get_pr_context(repo_url, pull_request_number)
    
    # Update progress
    self.update_state(
        state='PROGRESS',
        meta={'progress': 40}
    )
    
    # Analyze code
    issues = await ai_service.analyze_code(diff, pr_details["file_path"], context)
    
    # Update progress
    self.update_state(
        state='PROGRESS',
        meta={'progress': 80}
    )
    
    # Generate summary
    summary = ai_service.generate_summary(issues)
    
    return CodeAnalysis(
        status="completed",
        completion_percentage=100,
        issues=issues,
        summary=summary,
        estimated_review_time=len(issues) * 5  # Rough estimate: 5 minutes per issue
    ) 