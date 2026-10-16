
import streamlit as st

from src.pipeline import analyze_inquiry

st.set_page_config(
    page_title="Cynbit LeadIQ",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Cynbit LeadIQ")
st.caption("AI-powered lead qualification and response drafting")

st.info(
    "Prototype: analyze an inquiry, review its extracted details, "
    "and approve the suggested reply before using it."
)

examples = {
    "AI chatbot + CRM": (
        "We are a retail company looking for an AI chatbot integrated "
        "with our CRM. Our budget is ₹2 lakh and we want a prototype "
        "in four weeks."
    ),
    "Document processing": (
        "We need to automate invoice processing and extract data from "
        "PDF documents. We have not decided on a budget yet."
    ),
    "Unclear inquiry": (
        "We are interested in your services. Please contact us."
    ),
}

selected_example = st.selectbox(
    "Try a sample inquiry",
    ["Write my own"] + list(examples.keys()),
)

default_text = examples.get(selected_example, "")

inquiry = st.text_area(
    "Customer inquiry",
    value=default_text,
    height=160,
    max_chars=8000,
    placeholder="Paste a prospective customer's inquiry...",
)

if st.button("Analyze inquiry", type="primary"):
    if not inquiry.strip():
        st.warning("Please enter an inquiry.")
    else:
        with st.spinner("Analyzing inquiry..."):
            try:
                result = analyze_inquiry(inquiry)
                st.session_state["lead_result"] = result.model_dump()
                st.session_state["original_inquiry"] = inquiry
            except Exception as exc:
                # Show a useful error without exposing secrets or internals.
                st.error(f"Analysis failed: {exc}")


result = st.session_state.get("lead_result")
if result:
    if result.get("analysis_mode") == "Demo fallback":
        st.warning(
            "DEMO FALLBACK — Gemini was unavailable. "
            "Results use local heuristic rules, not live AI analysis."
        )
        if result.get("analysis_note"):
            st.caption(result["analysis_note"])
    else:
        st.success("Live Gemini analysis completed.")

    st.divider()
    st.subheader("Lead analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Service", result["service_category"])
    col2.metric("Priority", result["priority"])
    col3.metric("Priority score", f'{result["priority_score"]}/10')

    st.subheader("Extracted requirements")

    st.write("**Business goal**")
    st.write(result["business_goal"] or "Not identified")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Budget**")
        st.write(result["budget"] or "Not provided")

        st.write("**Timeline**")
        st.write(result["timeline"] or "Not provided")

    with col2:
        st.write("**Integrations / requirements**")
        st.write(", ".join(result["integrations"]) or "Not identified")

        st.write("**Missing information**")
        if result["missing_information"]:
            for item in result["missing_information"]:
                st.write(f"- {item}")
        else:
            st.write("No missing fields identified by the model.")

    st.subheader("Why this priority?")
    for reason in result["priority_reasons"]:
        st.write(f"- {reason}")

    st.subheader("Suggested reply")

    edited_reply = st.text_area(
        "Review and edit before use",
        value=result["draft_reply"],
        height=180,
        key="edited_reply",
    )

    st.download_button(
        "Download reply draft",
        data=edited_reply,
        file_name="cynbit_leadiq_reply.txt",
        mime="text/plain",
    )

    st.caption(
        "No email or CRM action is performed. Human review is required."
    )
