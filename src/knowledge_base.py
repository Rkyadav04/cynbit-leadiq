
CYNBIT_SERVICES = {
    "AI Automation": (
        "AI-powered automation and autonomous agent workflows."
    ),
    "Software Development": (
        "Custom software development and application solutions."
    ),
    "CRM Integration": (
        "CRM automation and integration workflows."
    ),
    "Document Processing": (
        "Automated document extraction and processing."
    ),
    "Voice AI": (
        "AI voice agents and voice-based customer interactions."
    ),
}

COMPANY_CONTEXT = """
You are assisting with inquiries for Cynbit, a technology company.
Use only the service descriptions supplied in this knowledge base.
These descriptions are a limited prototype knowledge base, not a
complete or independently verified company service catalogue.

Do not invent prices, guarantees, implementation timelines, client
references, or capabilities that are not explicitly supplied.
A human must review every reply before sending it.
"""


def get_service_context() -> str:
    return "\n".join(
        f"- {name}: {description}"
        for name, description in CYNBIT_SERVICES.items()
    )
