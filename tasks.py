import random
from typing import Dict, Any

TASKS_POOL = {
    "easy": [
        {
            "task_id": "easy_1",
            "difficulty": "easy",
            "job_description": (
                "Role: Junior Python Developer\n"
                "Company: TechStart Inc.\n"
                "We need a developer comfortable with Python and SQL to maintain our internal tools.\n"
                "Requirements: 1+ year experience, Python, SQL."
            ),
            "resume": (
                "Name: John Doe\n\n"
                "SUMMARY\n"
                "Data enthusiast with 2 years of experience in coding and database management.\n\n"
                "EXPERIENCE\n"
                "- Data Analyst at Fintech co. (2022-2024)\n"
                "- Built automation scripts in Python.\n"
                "- Managed SQL databases.\n\n"
                "SKILLS\n"
                "Python, SQL, JavaScript, Git."
            ),
            "requirements": {
                "required_skills": ["Python", "SQL"],
                "min_experience_years": 1,
                "must_be_suitable": True,
                "expected_missing": []
            }
        },
        {
            "task_id": "easy_2",
            "difficulty": "easy",
            "job_description": (
                "Role: Backend Intern (Node.js)\n"
                "Requirements: Node.js, Typescript. Experience not required but preferred."
            ),
            "resume": (
                "Name: Sam Rivers\n\n"
                "PROJECTS\n"
                "- Built a weather app using Node.js and Express.\n"
                "- Proficient in Typescript and Java.\n\n"
                "EDUCATION\n"
                "BS in Computer Science (2025 expected)."
            ),
            "requirements": {
                "required_skills": ["Node.js", "Typescript"],
                "min_experience_years": 0,
                "must_be_suitable": True,
                "expected_missing": []
            }
        }
    ],
    "medium": [
        {
            "task_id": "medium_1",
            "difficulty": "medium",
            "job_description": (
                "Role: Frontend Engineer\n"
                "Required Skills: JavaScript, React, CSS, HTML.\n"
                "Experience: 3+ years."
            ),
            "resume": (
                "Name: Jane Smith\n\n"
                "EXPERIENCE\n"
                "Web Developer at Creative Agency (2020-2024)\n"
                "- 4 years experience building professional websites.\n"
                "- Expert in HTML/CSS and JavaScript.\n"
                "- Experience with Vue.js and SASS.\n\n"
                "SKILLS\n"
                "JavaScript, HTML, CSS, SASS, Vue.js, Node.js."
            ),
            "requirements": {
                "required_skills": ["JavaScript", "CSS", "HTML", "React"],
                "min_experience_years": 3,
                "must_be_suitable": False,
                "expected_missing": ["React"]
            }
        },
        {
            "task_id": "medium_2",
            "difficulty": "medium",
            "job_description": (
                "Role: DevOps Engineer\n"
                "Skills: AWS, Docker, Terraform, Jenkins.\n"
                "Experience: 2+ years."
            ),
            "resume": (
                "Name: Mark Miller\n\n"
                "PROFESSIONAL EXPERIENCE\n"
                "Cloud Engineer at SkyCloud (2022-2024)\n"
                "- Managed AWS infrastructure for 2 years.\n"
                "- Built CI/CD pipelines using Jenkins.\n"
                "- Proficient in Docker but have never used Terraform.\n\n"
                "SKILLS\n"
                "AWS, Docker, Jenkins, Python, Bash."
            ),
            "requirements": {
                "required_skills": ["AWS", "Docker", "Terraform", "Jenkins"],
                "min_experience_years": 2,
                "must_be_suitable": False,
                "expected_missing": ["Terraform"]
            }
        }
    ],
    "hard": [
        {
            "task_id": "hard_1",
            "difficulty": "hard",
            "job_description": (
                "Role: Senior ML Engineer\n"
                "Required: Python, PyTorch, Kubernetes, AWS.\n"
                "Experience: 5+ years."
            ),
            "resume": (
                "Name: Alice Johnson\n\n"
                "SUMMARY\n"
                "5 years of experience in backend and ML engineering.\n\n"
                "WORK HISTORY\n"
                "- ML Engineer at AiCorp (3 years): Used PyTorch and Python.\n"
                "- Java Developer at Legacy Systems (2 years): Used AWS and Java.\n\n"
                "SKILLS\n"
                "Python, PyTorch, AWS, Java, C++, Docker.\n\n"
                "NOTE\n"
                "I am a quick learner but I do not know Kubernetes."
            ),
            "requirements": {
                "required_skills": ["Python", "PyTorch", "Kubernetes", "AWS"],
                "min_experience_years": 5,
                "must_be_suitable": False,
                "expected_missing": ["Kubernetes"]
            }
        },
        {
            "task_id": "hard_2",
            "difficulty": "hard",
            "job_description": (
                "Role: Cybersecurity Architect\n"
                "Required: CISSP certification, Wireshark, Metasploit, Python, 10+ years experience."
            ),
            "resume": (
                "Name: Robert Black\n\n"
                "EXPERIENCE\n"
                "Security Analyst at GovNet (12 years)\n"
                "- Expertise in Python and packet analysis with Wireshark.\n"
                "- I am not CISSP certified but planning to take it.\n"
                "- Have used Metasploit extensively for pen-testing.\n\n"
                "CERTIFICATIONS\n"
                "Security+, CEH."
            ),
            "requirements": {
                "required_skills": ["CISSP", "Wireshark", "Metasploit", "Python"],
                "min_experience_years": 10,
                "must_be_suitable": False,
                "expected_missing": ["CISSP"]
            }
        }
    ]
}

def get_task(difficulty: str) -> Dict[str, Any]:
    pool = TASKS_POOL.get(difficulty, TASKS_POOL["easy"])
    return random.choice(pool)
