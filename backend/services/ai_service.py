from typing import List, Dict
import openai
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from models import CodeIssue, SecurityRisk

class AICodeReviewService:
    def __init__(self):
        self.llm = OpenAI(temperature=0.3)
        self.review_prompt = PromptTemplate(
            input_variables=["code_diff", "file_path", "context"],
            template="""
            You are an expert code reviewer. Analyze the following code diff and provide detailed feedback:
            
            File: {file_path}
            Context: {context}
            
            Code Diff:
            {code_diff}
            
            Provide feedback in the following areas:
            1. Potential bugs or issues
            2. Security vulnerabilities
            3. Performance improvements
            4. Code style and best practices
            5. Architectural suggestions
            
            Format your response as a structured JSON object.
            """
        )
        
        self.security_prompt = PromptTemplate(
            input_variables=["code"],
            template="""
            Analyze the following code for security vulnerabilities:
            
            {code}
            
            Focus on:
            1. SQL injection
            2. XSS vulnerabilities
            3. Authentication issues
            4. Authorization flaws
            5. Data exposure risks
            
            Provide a detailed analysis with risk levels and mitigation strategies.
            """
        )
    
    async def analyze_code(self, code_diff: str, file_path: str, context: str) -> List[CodeIssue]:
        # Create review chain
        review_chain = LLMChain(llm=self.llm, prompt=self.review_prompt)
        
        # Get initial review
        review_result = await review_chain.arun(
            code_diff=code_diff,
            file_path=file_path,
            context=context
        )
        
        # Create security chain
        security_chain = LLMChain(llm=self.llm, prompt=self.security_prompt)
        
        # Get security analysis
        security_result = await security_chain.arun(code=code_diff)
        
        # Combine and process results
        return self._process_analysis_results(review_result, security_result)
    
    def _process_analysis_results(self, review_result: Dict, security_result: Dict) -> List[CodeIssue]:
        # Process and combine results into CodeIssue objects
        issues = []
        
        # Process review results
        for finding in review_result.get("findings", []):
            issues.append(
                CodeIssue(
                    file_path=finding["file_path"],
                    line_number=finding["line_number"],
                    issue_type=finding["type"],
                    description=finding["description"],
                    suggestion=finding["suggestion"],
                    risk_level=SecurityRisk(finding["risk_level"])
                )
            )
        
        # Process security results
        for vulnerability in security_result.get("vulnerabilities", []):
            issues.append(
                CodeIssue(
                    file_path=vulnerability["file_path"],
                    line_number=vulnerability["line_number"],
                    issue_type="security",
                    description=vulnerability["description"],
                    suggestion=vulnerability["mitigation"],
                    risk_level=SecurityRisk(vulnerability["risk_level"])
                )
            )
        
        return issues 