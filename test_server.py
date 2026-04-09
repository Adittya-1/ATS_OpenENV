import requests
import json

URL = "http://127.0.0.1:7860"

def test_flow():
    print("--- 1. Testing /reset ---")
    reset_res = requests.post(f"{URL}/reset", json={"difficulty": "easy"})
    if reset_res.status_code != 200:
        print(f"FAILED reset: {reset_res.text}")
        return
    
    task_data = reset_res.json()["observation"]
    print(f"Task ID: {task_data['task_id']}")
    
    print("\n--- 2. Testing /step with a payload ---")
    # Simulating a slightly 'messy' payload where an LLM might send experience as a string
    # instead of an int, to see if the server handles it.
    payload = {
        "action": {
            "matched_skills": ["Python", "SQL"],
            "missing_skills": [],
            "experience_years": 2,
            "is_suitable": True
        }
    }
    
    step_res = requests.post(f"{URL}/step", json=payload)
    print(f"Status: {step_res.status_code}")
    if step_res.status_code == 200:
        print("Grader Response:", json.dumps(step_res.json(), indent=2))
    else:
        print(f"FAILED step: {step_res.text}")

if __name__ == "__main__":
    test_flow()
