from models import AgentEvaluation
from typing import Dict, Any

def evaluate_action(action: AgentEvaluation, requirements: Dict[str, Any]) -> float:
    """
    Deterministically grade the agent's evaluation against ground truth.
    Returns a reward float strictly between 0 and 1.
    """
    # Safety check for missing/null action
    if not action:
        return 0.1

    try:
        required_skills = set(req.lower() for req in requirements["required_skills"])
        min_exp = requirements["min_experience_years"]
        expected_suitability = requirements["must_be_suitable"]

        agent_matched = set(s.lower() for s in action.matched_skills)
        agent_missing = set(s.lower() for s in action.missing_skills)
        agent_exp = action.experience_years
        agent_suitability = action.is_suitable

        score = 0.0
        
        agent_all_identified = agent_matched.union(agent_missing)

        # 1. Skill Extraction Score (0.3)
        if required_skills:
            found_required = agent_all_identified.intersection(required_skills)
            skill_extraction_score = len(found_required) / len(required_skills)
            score += skill_extraction_score * 0.3
        else:
            score += 0.3

        # 2. Experience Accuracy Score (0.2)
        if agent_exp >= min_exp:
            score += 0.2
        elif agent_exp >= min_exp - 1: # Partial credit for being very close
            score += 0.1
        
        # 3. Correct Categorization (Matched vs Missing) (0.3)
        expected_missing = set(m.lower() for m in requirements.get("expected_missing", []))

        correct_missing_ident = 0
        if expected_missing:
            found_missing = expected_missing.intersection(agent_missing)
            correct_missing_ident = len(found_missing) / len(expected_missing)
            
            actual_matched = required_skills - expected_missing
            false_negatives = agent_missing.intersection(actual_matched)
            correct_missing_ident -= (len(false_negatives) / len(required_skills)) * 0.5
            score += max(0, correct_missing_ident) * 0.3
        else:
            if not agent_missing:
                score += 0.3
            else:
                score += 0.1 

        # 4. Final Suitability Verdict (0.2)
        if agent_suitability == expected_suitability:
            score += 0.2
            
    except Exception as e:
        print(f"Error in evaluator: {e}")
        return 0.1

    # IMPORTANT: The hackathon validator requires scores to be strictly between 0 and 1.
    # We scale the 0.0-1.0 score to 0.1-0.9 range for maximum safety.
    final_reward = (score * 0.8) + 0.1
    return round(final_reward, 4)
