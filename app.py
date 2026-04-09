from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import os
import sys
from pydantic import BaseModel

# Add the current directory to sys.path to support flat-structure imports on Hugging Face
sys.path.append(os.path.dirname(__file__))
from models import ResetRequest, ResetResponse, StepRequest, StepResponse, StateResponse, TaskState
from tasks import get_task, TASKS_POOL
from evaluator import evaluate_action

app = FastAPI(title="OpenEnv ATS Resume Screener")

# Serve the Dashboard UI
@app.get("/", response_class=HTMLResponse)
def root():
    # Try multiple common locations for index.html
    # Since app.py is in server/, we search one level up too
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    possible_paths = [
        os.path.join(root_dir, "static", "index.html"),
        os.path.join(root_dir, "index.html"),
        os.path.join(os.path.dirname(__file__), "static", "index.html"),
        "index.html",
        "/app/static/index.html",
        "/app/index.html"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
                
    return f"<h1>OpenEnv ATS Environment is Running!</h1><p>Dashboard file missing. Searched in: {possible_paths}</p>"

@app.get("/tasks-data")
def tasks_data():
    return TASKS_POOL

# Global variables for state management 
current_task_state = None
is_done = True
start_time = 0

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
    
    # Log incoming request for debugging
    print(f"DEBUG: Received /step with action: {req.action}")
    
    if current_task_state is None or is_done:
        raise HTTPException(status_code=400, detail="Environment is not initialized or is done. Call /reset first.")
        
    # Robust type handling for experience_years
    try:
        val = req.action.experience_years
        if isinstance(val, str):
            import re
            nums = re.findall(r"\d+", val)
            req.action.experience_years = int(nums[0]) if nums else 0
        else:
            req.action.experience_years = int(float(val))
    except (ValueError, TypeError, IndexError):
        req.action.experience_years = 0

    reward = evaluate_action(req.action, current_task_state.requirements)
    is_done = True # In this ATS task, it's a 1-step episode
    
    print(f"DEBUG: Calculated reward: {reward}")
    
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

def main():
    import uvicorn
    # The validator expects the server to run on 7860 for Hugging Face
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
