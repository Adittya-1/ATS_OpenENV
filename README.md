# OpenEnv Resume Screening / ATS Environment

This is a real-world task environment built using the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework for the Scalar OpenEnv Hackathon Round 1.

## Environment Description

The environment simulates a real-world **Applicant Tracking System (ATS)**. It evaluates large language model agents on their ability to accurately parse and score candidate resumes against various job descriptions. The agent's task is to extract matched skills, identify missing skills, calculate relevant experience years, and decide on candidate suitability based on the job requirements. The environment then computes a deterministic reward score based on how accurately the agent evaluated the candidate.

## Difficulties
The environment includes a pool of 6 distinct tasks (2 per difficulty level) to ensure robustness:
- **Easy**: 
  - `easy_1`: Junior Python Developer (TechStart Inc)
  - `easy_2`: Backend Intern (Node.js)
- **Medium**: 
  - `medium_1`: Frontend Engineer (Missing React)
  - `medium_2`: DevOps Engineer (Missing Terraform)
- **Hard**: 
  - `hard_1`: Senior ML Engineer (Missing Kubernetes)
  - `hard_2`: Cybersecurity Architect (Missing CISSP)

## Observation Space

The observation space is a JSON object `TaskState` provided upon `/reset` and `/state`:
```json
{
  "task_id": "string",
  "difficulty": "string (easy | medium | hard)",
  "job_description": "string",
  "resume": "string",
  "requirements": {
    "required_skills": ["string"],
    "min_experience_years": "integer",
    "must_be_suitable": "boolean"
  }
}
```

## Action Space

The action space requires the agent to submit a strict JSON representation of its evaluation via `/step`, formatted as follows:
```json
{
  "matched_skills": ["string (skills found)"],
  "missing_skills": ["string (skills missing)"],
  "experience_years": "integer (years of experience extracted)",
  "is_suitable": "boolean (whether the candidate met all requirements)"
}
```

## Setup & Local Testing

### Requirements
- Docker OR Python 3.10+
- Environment Variables needed for `inference.py`:
  - `API_BASE_URL`: URL to the environment API (defaults to http://localhost:7860)
  - `MODEL_NAME`: Hugging Face / OpenAI Model name to use (defaults to gpt-3.5-turbo)
  - `HF_TOKEN`: API key for model inference

### Running using Server
```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
```

### Running Inference Script
In a separate terminal:
```bash
export API_BASE_URL="http://localhost:7860"
export MODEL_NAME="gpt-3.5-turbo"
export HF_TOKEN="your_token_here"
python inference.py
```
This script will produce `[START]`, `[STEP]`, and `[END]` logging artifacts.

### Running with Docker (Production/Submission Setup)
```bash
docker build -t openenv-ats .
docker run -p 7860:7860 openenv-ats
```

## Reward Function

The reward function evaluates the `action` input using deterministic scoring yielding a float between `0.0` and `1.0`:
1. **Skill Matching (`0.25`)**: Did the agent correctly partition the `required_skills` into `matched_skills` and `missing_skills`?
2. **Experience (`0.25`)**: Did the agent correctly extract the correct number of years of experience?
3. **Missing Skills Identification (`0.25`)**: Did the agent accurately spot the *absence* of specific required skills?
4. **Final Decision (`0.25`)**: Is the ultimate `is_suitable` boolean verdict correct?
