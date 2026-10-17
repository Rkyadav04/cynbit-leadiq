
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from src.pipeline import analyze_inquiry


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_FILE = BASE_DIR / "data" / "sample_inquiries.json"

st.set_page_config(
    page_title="Cynbit LeadIQ",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --bg: #07111b;
        --panel: #0d1d2c;
        --panel2: #102334;
        --teal: #8be0d0;
        --teal-strong: #35b9a4;
        --text: #eff6f8;
        --muted: #91a7b5;
        --border: rgba(175,196,210,.15);
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(53,185,164,.09),
                transparent 27%
            ),
            #07111b;
        color: var(--text);
        font-family: "DM Sans", sans-serif;
    }

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }

    .block-container {
        max-width: 1480px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    h1, h2, h3 {
        font-family: "Manrope", sans-serif !important;
        color: #eff6f8 !important;
        letter-spacing: -.5px;
    }

    p, li, label {
        color: #c4d4dc;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: #091725;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .brand-title {
        font-family: "Manrope", sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #f4fafb;
        letter-spacing: -.5px;
    }

    .brand-subtitle {
        color: #718b9b;
        font-size: .7rem;
        letter-spacing: 1.1px;
        text-transform: uppercase;
        margin-top: .35rem;
    }

    .brand-symbol {
        color: #071823;
        background: linear-gradient(145deg,#8be0d0,#35b9a4);
        border-radius: 10px;
        padding: .45rem .7rem;
        font-family: "Manrope", sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
    }

    .sidebar-label {
        color: #718b9b;
        font-size: .65rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .sidebar-panel {
        border: 1px solid var(--border);
        background: rgba(255,255,255,.02);
        border-radius: 11px;
        padding: 1rem;
    }

    .sidebar-small {
        color: #8ca3b2;
        font-size: .76rem;
        line-height: 1.6;
    }

    /* Hero */

    .hero-shell {
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.7rem;
        background:
            radial-gradient(
                circle at 83% 45%,
                rgba(53,185,164,.11),
                transparent 27%
            ),
            linear-gradient(125deg,#0d2030,#091622);
        margin-bottom: 1.5rem;
    }

    .eyebrow {
        color: var(--teal);
        font-size: .67rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero-title {
        font-family: "Manrope", sans-serif;
        color: #f3f8fa;
        font-size: clamp(2.3rem, 4.5vw, 4.2rem);
        font-weight: 700;
        line-height: 1.08;
        letter-spacing: -2.5px;
        margin: .9rem 0 1rem;
    }

    .hero-accent {
        color: var(--teal);
    }

    .hero-description {
        color: #a7bdc9;
        font-size: .95rem;
        line-height: 1.8;
        max-width: 680px;
    }

    .hero-status {
        color: #91a9b7;
        font-size: .66rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        margin-top: 1.5rem;
    }

    .system-panel {
        background: rgba(5,19,30,.62);
        border: 1px solid rgba(139,224,208,.23);
        border-radius: 15px;
        padding: 1.2rem;
    }

    .system-heading {
        color: #b4c8d2;
        font-size: .65rem;
        font-weight: 700;
        letter-spacing: 1.3px;
    }

    .system-core {
        width: 84px;
        height: 84px;
        margin: 1.6rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 24px;
        background: linear-gradient(145deg,#8be0d0,#35b9a4);
        color: #102338;
        font-family: "Manrope", sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        box-shadow: 0 0 36px rgba(53,185,164,.15);
    }

    .system-line {
        display: flex;
        justify-content: space-between;
        gap: .5rem;
        padding: .75rem 0;
        border-bottom: 1px solid rgba(175,196,210,.1);
        font-size: .73rem;
    }

    .system-line:last-child {
        border-bottom: none;
    }

    .system-line span {
        color: #829bab;
    }

    .system-line strong {
        color: #e5eff3;
        font-weight: 500;
        text-align: right;
    }

    /* Section headers */

    .section-kicker {
        color: var(--teal);
        font-size: .65rem;
        font-weight: 700;
        letter-spacing: 1.6px;
        margin-bottom: .4rem;
    }

    .section-subtitle {
        color: #829aaa;
        font-size: .83rem;
        line-height: 1.65;
    }

    /* Cards */

    .panel {
        background: rgba(13,29,44,.82);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.1rem;
        height: 100%;
    }

    .panel-label {
        color: #829aaa;
        font-size: .64rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .panel-value {
        color: #eef6f8;
        font-family: "Manrope", sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        line-height: 1.5;
        margin-top: .55rem;
        overflow-wrap: anywhere;
    }

    .teal-text {
        color: var(--teal);
    }

    /* Inputs */

    div[data-testid="stTextArea"] textarea {
        background: #0b1a28 !important;
        color: #edf5f7 !important;
        border: 1px solid rgba(175,196,210,.2) !important;
        border-radius: 10px !important;
        line-height: 1.65 !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: rgba(139,224,208,.6) !important;
        box-shadow: 0 0 0 1px rgba(139,224,208,.15) !important;
    }

    div[data-baseweb="select"] > div {
        background: #0b1a28 !important;
        border-color: var(--border) !important;
        border-radius: 9px !important;
    }

    /* Buttons */

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 9px;
        font-weight: 700;
        transition: .18s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg,#8be0d0,#5ed1bd);
        border: 1px solid #35b9a4;
        color: #071823;
    }

    .stButton > button[kind="primary"]:hover {
        background: #a0e8da;
        border-color: #a0e8da;
        color: #071823;
        transform: translateY(-1px);
    }

    .stDownloadButton > button {
        background: transparent;
        color: var(--teal);
        border: 1px solid rgba(139,224,208,.3);
    }

    /* Result and status panels */

    .result-note {
        color: #91a7b5;
        font-size: .75rem;
        line-height: 1.65;
    }

    .app-footer {
        border-top: 1px solid var(--border);
        margin-top: 3.5rem;
        padding-top: 1.2rem;
        color: #647e8e;
        font-size: .65rem;
        letter-spacing: .7px;
    }

    @media(max-width: 850px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-shell {
            padding: 1.5rem;
        }

        .hero-title {
            font-size: 2.5rem;
            letter-spacing: -1.5px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA HELPERS
# ============================================================

def read_field(obj: Any, key: str, default: Any = None) -> Any:
    """Read a field from either a dictionary or a model object."""
    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


def to_plain_dict(obj: Any) -> dict:
    """Convert a Pydantic model or mapping into a JSON-friendly dict."""
    if isinstance(obj, dict):
        return obj

    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")

    if hasattr(obj, "dict"):
        return obj.dict()

    raise TypeError(
        "The analysis result is not a supported model or dictionary."
    )


def display_value(value: Any, default: str = "Not identified") -> str:
    if value is None:
        return default

    if isinstance(value, str):
        value = value.strip()
        return value if value else default

    return str(value)


def display_list(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, (list, tuple, set)):
        return [
            str(item).strip()
            for item in value
            if item is not None and str(item).strip()
        ]

    if isinstance(value, str) and value.strip():
        return [value.strip()]

    return []


def load_samples() -> list:
    """Read the existing sample inquiry JSON file."""
    if not SAMPLE_FILE.exists():
        return []

    try:
        with SAMPLE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            # Support common sample JSON layouts.
            for key in ("samples", "inquiries", "examples"):
                if isinstance(data.get(key), list):
                    return data[key]

        return []

    except (OSError, json.JSONDecodeError):
        return []


def sample_text(sample: Any) -> str:
    if isinstance(sample, str):
        return sample

    if isinstance(sample, dict):
        for key in (
            "inquiry",
            "text",
            "message",
            "customer_inquiry",
            "query",
            "content",
        ):
            value = sample.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    return ""


def sample_label(sample: Any, index: int) -> str:
    if isinstance(sample, dict):
        for key in ("title", "name", "label", "company"):
            value = sample.get(key)
            if value:
                return f"{index + 1:02d} — {value}"

    return f"{index + 1:02d} — Sample inquiry"


def score_band(score: float) -> tuple[str, str]:
    if score >= 8:
        return "HIGH PRIORITY", "High"
    if score >= 5:
        return "MEDIUM PRIORITY", "Medium"
    return "NEEDS DISCOVERY", "Low"


# ============================================================
# SESSION STATE
# ============================================================

if "inquiry_text" not in st.session_state:
    st.session_state.inquiry_text = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "reviewed_reply" not in st.session_state:
    st.session_state.reviewed_reply = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    logo_col, brand_col = st.columns([0.55, 2.45], vertical_alignment="center")

    with logo_col:
        st.markdown(
            '<div class="brand-symbol">C</div>',
            unsafe_allow_html=True,
        )

    with brand_col:
        st.markdown(
            """
            <div class="brand-title">
                CYNBIT <span style="color:#8be0d0">LeadIQ</span>
            </div>
            <div class="brand-subtitle">
                Lead intelligence prototype
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<div class="sidebar-label">Workspace</div>',
        unsafe_allow_html=True,
    )
    st.markdown("◈  **Lead Intelligence**")
    st.caption("Extract, qualify and prepare a response.")

    st.markdown("◇  Qualification Engine")
    st.caption("Structured signals and priority reasoning.")

    st.markdown("◇  Response Architect")
    st.caption("Human-reviewed response drafting.")

    st.divider()

    st.markdown(
        '<div class="sidebar-label">Prototype status</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-panel">
            <div class="sidebar-small">
                <span style="color:#8be0d0">●</span>
                Application ready
            </div>
            <div class="sidebar-small">
                Human review: required
            </div>
            <div class="sidebar-small">
                CRM writes: disabled
            </div>
            <div class="sidebar-small">
                Email sending: disabled
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        """
        <div class="sidebar-small">
            AI/ML engineering proof of concept.<br><br>
            LeadIQ supports human decision-making. It does not
            autonomously contact prospects or update CRM records.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

hero_left, hero_right = st.columns([1.45, 0.8], gap="large")

with hero_left:
    st.markdown(
        """
        <div class="hero-shell">
            <div class="eyebrow">
                THE OPTIMISTIC ARCHITECT / LEADIQ
            </div>
            <div class="hero-title">
                Architecting better<br>
                <span class="hero-accent">lead decisions.</span>
            </div>
            <div class="hero-description">
                Transform unstructured customer inquiries into
                actionable lead intelligence. Extract requirements,
                identify information gaps, prioritize opportunities,
                and prepare thoughtful responses with a human in control.
            </div>
            <div class="hero-status">
                ◉ &nbsp; LEAD INTELLIGENCE WORKSPACE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        """
        <div class="hero-shell">
            <div class="system-panel">
                <div class="system-heading">
                    SYSTEM OVERVIEW &nbsp; / &nbsp; LEADIQ
                </div>
                <div class="system-core">LQ</div>
                <div class="system-line">
                    <span>01 / INPUT</span>
                    <strong>Inquiry capture</strong>
                </div>
                <div class="system-line">
                    <span>02 / ENGINE</span>
                    <strong>Lead qualification</strong>
                </div>
                <div class="system-line">
                    <span>03 / OUTPUT</span>
                    <strong>Response draft</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-kicker">01 / DISCOVERY</div>',
    unsafe_allow_html=True,
)
st.header("Qualify a prospective inquiry")
st.markdown(
    '<div class="section-subtitle">'
    'Load a sample or paste a customer message. Review the extracted '
    'details before making any business decision.'
    '</div>',
    unsafe_allow_html=True,
)
st.write("")

samples = load_samples()

sample_options = ["— Enter inquiry manually —"]
sample_lookup = {}

for index, sample in enumerate(samples):
    label = sample_label(sample, index)

    # Ensure labels remain unique.
    while label in sample_lookup:
        label += " ·"

    sample_options.append(label)
    sample_lookup[label] = sample_text(sample)

sample_col, load_col = st.columns([3, 1], vertical_alignment="bottom")

with sample_col:
    selected_sample = st.selectbox(
        "Sample inquiry",
        options=sample_options,
        index=0,
        help="Choose an example to load into the inquiry editor.",
    )

with load_col:
    load_clicked = st.button(
        "Load sample",
        use_container_width=True,
        disabled=selected_sample == sample_options[0],
    )

if load_clicked and selected_sample in sample_lookup:
    st.session_state.inquiry_text = sample_lookup[selected_sample]
    st.session_state.analysis_result = None
    st.session_state.reviewed_reply = ""

input_col, guide_col = st.columns([1.55, 0.75], gap="large")

with input_col:
    inquiry = st.text_area(
        "Customer inquiry",
        key="inquiry_text",
        height=230,
        placeholder=(
            "Example: We are a retail company looking for an AI chatbot "
            "integrated with our CRM. Our budget is ₹2 lakh and we want "
            "a prototype in four weeks..."
        ),
        help="Paste the customer's original message. Avoid including passwords or secrets.",
    )

    run_clicked = st.button(
        "Analyze opportunity  →",
        type="primary",
        use_container_width=True,
    )

with guide_col:
    st.markdown("### Qualification workflow")

    with st.container(border=True):
        st.markdown("**01 · Understand**")
        st.caption("Identify the service and business context.")

        st.markdown("**02 · Structure**")
        st.caption("Extract budget, timeline and integrations.")

        st.markdown("**03 · Qualify**")
        st.caption("Score the opportunity and find information gaps.")

        st.markdown("**04 · Respond**")
        st.caption("Prepare a draft for human review.")


# ============================================================
# ANALYSIS EXECUTION
# ============================================================

if run_clicked:
    cleaned_inquiry = inquiry.strip()

    if not cleaned_inquiry:
        st.warning("Enter a customer inquiry before running the analysis.")

    elif len(cleaned_inquiry) > 8000:
        st.error(
            "This inquiry is too long for the current prototype. "
            "Please keep it under 8,000 characters."
        )

    else:
        try:
            with st.spinner(
                "Analyzing the inquiry and structuring the opportunity..."
            ):
                result = analyze_inquiry(cleaned_inquiry)
                result_dict = to_plain_dict(result)

            st.session_state.analysis_result = result_dict
            st.session_state.reviewed_reply = str(
                result_dict.get("draft_reply") or ""
            )

        except Exception as exc:
            st.session_state.analysis_result = None
            st.session_state.reviewed_reply = ""

            st.error(
                "Analysis failed. Check the application logs and API "
                "configuration, then try again."
            )
            st.caption(f"Error type: {type(exc).__name__}")


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.analysis_result

if result:
    st.write("")
    st.divider()

    st.markdown(
        '<div class="section-kicker">02 / QUALIFICATION</div>',
        unsafe_allow_html=True,
    )
    st.header("Opportunity intelligence")
    st.markdown(
        '<div class="section-subtitle">'
        'A structured view of the customer inquiry. Treat extracted '
        'information as a starting point for review, not verified fact.'
        '</div>',
        unsafe_allow_html=True,
    )

    analysis_mode = display_value(
        read_field(result, "analysis_mode"),
        "Mode not reported",
    )
    analysis_note = display_value(
        read_field(result, "analysis_note"),
        "",
    )

    if analysis_mode.lower() == "live gemini":
        st.success("LIVE GEMINI ANALYSIS")
        if analysis_note:
            st.caption(analysis_note)

    elif analysis_mode.lower() == "demo fallback":
        st.warning(
            "DEMO FALLBACK — LOCAL HEURISTICS. "
            "These results were generated using local rules, not live LLM analysis."
        )
        if analysis_note:
            st.caption(analysis_note)

    else:
        st.info(
            f"Analysis mode: {analysis_mode}. "
            "Check the pipeline configuration to confirm which engine ran."
        )
        if analysis_note:
            st.caption(analysis_note)

    service_category = display_value(
        read_field(result, "service_category")
    )
    business_goal = display_value(
        read_field(result, "business_goal")
    )
    budget = display_value(read_field(result, "budget"))
    timeline = display_value(read_field(result, "timeline"))

    integrations = display_list(read_field(result, "integrations"))
    missing_information = display_list(
        read_field(result, "missing_information")
    )
    priority_reasons = display_list(
        read_field(result, "priority_reasons")
    )

    draft_reply = display_value(
        read_field(result, "draft_reply"),
        "",
    )

    try:
        priority_score = float(read_field(result, "priority_score", 0))
    except (ValueError, TypeError):
        priority_score = 0.0

    priority_score = max(0.0, min(10.0, priority_score))
    band, _ = score_band(priority_score)

    # --------------------------------------------------------
    # KEY SIGNALS
    # --------------------------------------------------------

    st.markdown("### Key signals")

    metric_cols = st.columns(4, gap="medium")

    metrics = [
        ("SERVICE CATEGORY", service_category),
        ("BUDGET", budget),
        ("TIMELINE", timeline),
        (
            "INTEGRATIONS",
            ", ".join(integrations) if integrations else "Not identified",
        ),
    ]

    for col, (label, value) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f'<div class="panel-label">{label}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="panel-value">{value}</div>',
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    st.write("")
    st.markdown("### Opportunity priority")

    score_col, explanation_col = st.columns([1, 2], gap="large")

    with score_col:
        st.metric(
            label="Heuristic priority score",
            value=f"{priority_score:g} / 10",
            help=(
                "This is a heuristic qualification signal. "
                "It is not a conversion probability or sales forecast."
            ),
        )
        st.progress(priority_score / 10)
        st.caption(f"Priority band: **{band}**")

    with explanation_col:
        st.markdown("**Why this score?**")

        if priority_reasons:
            for reason in priority_reasons:
                st.markdown(f"- {reason}")
        else:
            st.caption("No priority reasons were provided by the pipeline.")

        st.caption(
            "Validate the score against your actual sales process before "
            "using it for prioritization."
        )

    # --------------------------------------------------------
    # DISCOVERY DETAILS
    # --------------------------------------------------------

    st.write("")
    st.divider()

    st.markdown(
        '<div class="section-kicker">03 / DISCOVERY MAP</div>',
        unsafe_allow_html=True,
    )
    st.header("Requirements and information gaps")

    details_col, gaps_col = st.columns([1.1, 0.9], gap="large")

    with details_col:
        with st.container(border=True):
            st.markdown("**Business goal**")
            st.write(business_goal)

            st.divider()
            st.markdown("**Integrations identified**")

            if integrations:
                for integration in integrations:
                    st.markdown(f"- {integration}")
            else:
                st.caption("No integrations identified.")

    with gaps_col:
        with st.container(border=True):
            st.markdown("**Information to clarify**")

            if missing_information:
                for item in missing_information:
                    st.markdown(f"- {item}")
            else:
                st.success(
                    "No information gaps were returned by the current analysis."
                )

            st.caption(
                "Confirm this list with the customer before finalizing scope."
            )

    # --------------------------------------------------------
    # RESPONSE DRAFT
    # --------------------------------------------------------

    st.write("")
    st.divider()

    st.markdown(
        '<div class="section-kicker">04 / RESPONSE ARCHITECT</div>',
        unsafe_allow_html=True,
    )
    st.header("Suggested customer response")
    st.markdown(
        '<div class="section-subtitle">'
        'Edit the draft as needed. This prototype does not send emails '
        'or contact customers automatically.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Initialize the editor from the latest analysis without overwriting
    # edits on ordinary Streamlit reruns.
    if "reviewed_reply" not in st.session_state:
        st.session_state.reviewed_reply = draft_reply

    reviewed_reply = st.text_area(
        "Edit response before use",
        key="reviewed_reply",
        height=240,
    )

    download_col, json_col = st.columns(2)

    with download_col:
        st.download_button(
            "Download response draft",
            data=reviewed_reply,
            file_name="cynbit_leadiq_response.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with json_col:
        report_json = json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

        st.download_button(
            "Download analysis JSON",
            data=report_json,
            file_name="cynbit_leadiq_analysis.json",
            mime="application/json",
            use_container_width=True,
        )

    st.info(
        "Human review required. Verify factual claims, delivery timelines, "
        "pricing and commitments before using the suggested response."
    )


# ============================================================
# EMPTY STATE
# ============================================================

else:
    st.write("")

    with st.container(border=True):
        st.markdown("### Your qualification workspace is ready")
        st.markdown(
            "Enter a customer inquiry above or load a sample, then select "
            "**Analyze opportunity** to generate structured results."
        )

        st.caption(
            "The analysis engine depends on your existing pipeline and "
            "configured API credentials. If the LLM provider is unavailable, "
            "the application should clearly report whether a fallback ran."
        )


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.divider()

footer_left, footer_right = st.columns([1, 1])

with footer_left:
    st.caption("CYNBIT LEADIQ · AI/ML ENGINEERING PROOF OF CONCEPT")

with footer_right:
    st.caption(
        "Human-in-the-loop · No automatic emails · No CRM writes"
    )
