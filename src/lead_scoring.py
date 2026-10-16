
def calculate_priority(lead: dict) -> dict:
    """Score a lead using transparent, configurable rules."""

    score = 0
    reasons = []

    goal = (lead.get("business_goal") or "").strip()
    timeline = (lead.get("timeline") or "").strip()
    budget = (lead.get("budget") or "").strip()
    integrations = lead.get("integrations") or []
    category = lead.get("service_category", "Unclear")

    if goal and len(goal) >= 20:
        score += 2
        reasons.append("A reasonably clear business goal was provided.")

    if timeline:
        score += 2
        reasons.append("A timeline was provided.")

    if budget:
        score += 2
        reasons.append("Budget information was provided.")

    if integrations:
        score += 2
        reasons.append("Technical requirements or integrations were identified.")

    if category not in ("Other", "Unclear"):
        score += 2
        reasons.append("The inquiry matches an identifiable service category.")

    if score >= 7:
        priority = "High"
    elif score >= 4:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "priority": priority,
        "priority_score": score,
        "priority_reasons": reasons,
    }
