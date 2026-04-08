from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import os
from pydantic import BaseModel
from models import ResetRequest, ResetResponse, StepRequest, StepResponse, StateResponse, TaskState
from tasks import get_task
from evaluator import evaluate_action

app = FastAPI(title="OpenEnv ATS Resume Screener")

# Serve the Dashboard UI
@app.get("/", response_class=HTMLResponse)
def root():
    # Try multiple common locations for index.html
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "static", "index.html"),
        os.path.join(os.path.dirname(__file__), "index.html"),
        "index.html",
        "/app/static/index.html",
        "/app/index.html"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
                
    return "<h1>OpenEnv ATS Environment is Running!</h1><p>Dashboard file missing. Please ensure 'index.html' is uploaded to the 'static' folder or the root.</p>"

@app.get("/tasks-data")
def tasks_data():
    from tasks import TASKS_POOL
    return TASKS_POOL

# Global variables for state management 
current_task_state = None
is_done = True

@app.post("/reset", response_model=ResetResponse)
def reset(req: ResetRequest = None):
    global current_task_state, is_done
    difficulty = req.difficulty if req and req.difficulty else "easy"
    
    task_data = get_task(difficulty)
    current_task_state = TaskState(**task_data)
    is_done = False
    
    return ResetResponse(observation=current_task_state)

@app.post("/step", response_model=StepResponse)
def step(req: StepRequest):
    global current_task_state, is_done
    
    if current_task_state is None or is_done:
        raise HTTPException(status_code=400, detail="Environment is not initialized or is done. Call /reset first.")
        
    reward = evaluate_action(req.action, current_task_state.requirements)
    is_done = True # In this ATS task, it's a 1-step episode
    
    return StepResponse(
        observation=current_task_state,
        reward=reward,
        done=is_done,
        info={"message": "Evaluation processed"}
    )

@app.get("/state", response_model=StateResponse)
def state():
    if current_task_state is None:
        raise HTTPException(status_code=400, detail="Environment is not initialized. Call /reset first.")
        
    return StateResponse(
        observation=current_task_state,
        done=is_done
    )

@app.get("/health")
def health():
    return {"status": "ok"}
