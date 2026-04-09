from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Agent Action (Output) Models ---
class AgentEvaluation(BaseModel):
    matched_skills: List[str] = Field(default_factory=list, description="List of required skills found in the resume.")
    missing_skills: List[str] = Field(default_factory=list, description="List of required skills missing from the resume.")
    experience_years: Any = Field(default=0, description="Total years of relevant experience identified.")
    is_suitable: bool = Field(default=False, description="Whether the candidate is suitable for the role.")

# --- Environment State Models ---
class TaskState(BaseModel):
    task_id: str
    difficulty: str
    job_description: str
    resume: str
    requirements: Dict[str, Any]

# --- API Request/Response Models ---
class ResetRequest(BaseModel):
    difficulty: Optional[str] = None  # e.g. "easy", "medium", "hard"

class ResetResponse(BaseModel):
    observation: TaskState

class StepRequest(BaseModel):
    action: AgentEvaluation

class StepResponse(BaseModel):
    observation: TaskState
    reward: float
    done: bool
    info: Dict[str, Any]

class StateResponse(BaseModel):
    observation: TaskState
    done: bool
