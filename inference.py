import os
import json
import requests
from openai import OpenAI
import time

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

print("[START] Inference Process Started")

# Fallback fake client if no token provided (for local testing without keys)
# The hackathon will provide an actual API key via HF_TOKEN
if not HF_TOKEN:
    print("Warning: HF_TOKEN not found, assuming local or mock run.")
else:
    # Adjust base_url if needed by OpenEnv, otherwise default OpenAI endpoint
    # Sometimes HF_TOKEN is used as an OpenAI compatible api_key
    pass

client = OpenAI(
    api_key=HF_TOKEN if HF_TOKEN else "mock-token"
    # base_url="https://api.openai.com/v1" # Customize if needed
)

def evaluate_with_llm(job_description: str, resume: str) -> dict:
    """
    Call the LLM to get an evaluation of the candidate.
    """
    system_prompt = (
        "You are an ATS (Applicant Tracking System). "
        "Review the job description and the candidate's resume. "
        "Extract the following into a valid JSON object EXACTLY matching this schema:\n"
        "{\n"
        '  "matched_skills": ["Skill1", "Skill2"],\n'
        '  "missing_skills": ["Skill3"],\n'
        '  "experience_years": 3,\n'
        '  "is_suitable": true\n'
        "}\n"
        "If a candidate lacks any required skills or does not meet the minimum experience, is_suitable MUST be false."
    )
    
    user_prompt = (
        f"Job Description:\n{job_description}\n\n"
        f"Resume:\n{resume}\n"
    )

    try:
        # Mocking logic if no real token for successful local execution without hitting API limit
        if HF_TOKEN is None or HF_TOKEN == "":
            return {
                "matched_skills": ["Python", "SQL", "JavaScript"],
                "missing_skills": [],
                "experience_years": 2,
                "is_suitable": True
            }

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"Error during LLM call: {e}")
        # Always return valid structure to prevent crash
        return {
            "matched_skills": [],
            "missing_skills": [],
            "experience_years": 0,
            "is_suitable": False
        }

def run_task(difficulty: str):
    print(f"\n[STEP] Starting Task: {difficulty}")
    
    # 1. Reset Environment
    try:
        reset_res = requests.post(f"{API_BASE_URL}/reset", json={"difficulty": difficulty})
        reset_res.raise_for_status()
        state = reset_res.json()["observation"]
    except Exception as e:
        print(f"Failed to reset environment for difficulty {difficulty}: {e}")
        return

    # 2. Extract context
    job_desc = state["job_description"]
    resume = state["resume"]
    
    # 3. Agent Action
    agent_action_payload = evaluate_with_llm(job_desc, resume)
    
    print(f"Agent Action Context Generated: {json.dumps(agent_action_payload)}")
    
    # 4. Step Step Action
    try:
        step_res = requests.post(f"{API_BASE_URL}/step", json={"action": agent_action_payload})
        step_res.raise_for_status()
        result = step_res.json()
        reward = result["reward"]
        done = result["done"]
        print(f"Step Result - Reward: {reward}, Done: {done}")
    except Exception as e:
        print(f"Failed to execute step: {e}")
        return

if __name__ == "__main__":
    # Wait for the server to be ready just in case
    time.sleep(2)
    difficulties = ["easy", "medium", "hard"]
    for diff in difficulties:
        run_task(diff)
        
    print("\n[END] Inference Process Completed")
