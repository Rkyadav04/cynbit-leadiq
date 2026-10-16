
from src.lead_scoring import calculate_priority


def test_complete_lead_gets_high_priority():
    lead = {
        "business_goal": "Automate customer support for our retail business",
        "timeline": "4 weeks",
        "budget": "₹2 lakh",
        "integrations": ["CRM"],
        "service_category": "AI Automation",
    }

    result = calculate_priority(lead)

    assert result["priority"] == "High"
    assert result["priority_score"] == 10


def test_missing_details_get_lower_priority():
    lead = {
        "business_goal": "",
        "timeline": None,
        "budget": None,
        "integrations": [],
        "service_category": "Unclear",
    }

    result = calculate_priority(lead)

    assert result["priority"] == "Low"
    assert result["priority_score"] == 0


def test_score_is_never_above_ten():
    lead = {
        "business_goal": "Automate our customer service workflow",
        "timeline": "2 weeks",
        "budget": "₹1 lakh",
        "integrations": ["CRM", "Email"],
        "service_category": "CRM Integration",
    }

    result = calculate_priority(lead)

    assert 0 <= result["priority_score"] <= 10
