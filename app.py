import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.sop_agent import SOPAgent
from agents.ticket_agent import TicketAgent
from agents.orchestrator import IncidentOrchestrator

st.set_page_config(
    page_title="AI Incident Investigation Copilot",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AI Incident Investigation Copilot")
st.markdown("*Powered by Azure OpenAI GPT-4o + Multi-Agent RAG Architecture*")
st.divider()

@st.cache_resource
def load_system():
    orchestrator = IncidentOrchestrator()
    orchestrator.sop_agent.load_sops()
    orchestrator.ticket_agent.load_tickets()
    return orchestrator

with st.spinner("Loading AI agents and knowledge base..."):
    orchestrator = load_system()

st.success("✅ AI Agents Ready — SOP Agent | Ticket Agent | Orchestrator")
st.divider()

st.subheader("📋 Incident Input")
incident = st.text_area(
    "Describe the incident:",
    placeholder="e.g. Users are unable to login. VPN authentication failures increasing. MFA prompts timing out.",
    height=120
)

col1, col2, col3 = st.columns(3)
with col2:
    investigate_btn = st.button("🔍 Investigate Incident", type="primary", use_container_width=True)

if investigate_btn and incident:
    st.divider()

    col_sop, col_ticket = st.columns(2)

    with col_sop:
        with st.spinner("🔍 SOP Agent retrieving procedures..."):
            sop_results = orchestrator.sop_agent.retrieve(incident)
        st.subheader("📖 SOP Agent")
        st.success(f"Found {len(sop_results)} relevant SOPs")
        for i, sop in enumerate(sop_results, 1):
            with st.expander(f"SOP Reference {i}"):
                st.text(sop[:500] + "...")

    with col_ticket:
        with st.spinner("🎫 Ticket Agent finding similar incidents..."):
            ticket_results = orchestrator.ticket_agent.find_similar(incident)
        st.subheader("🎫 Ticket Agent")
        st.success(f"Found {len(ticket_results)} similar past incidents")
        for i, ticket in enumerate(ticket_results, 1):
            with st.expander(f"Past Incident {i} — {ticket['category']}"):
                st.markdown(f"**Description:** {ticket['description']}")
                st.markdown(f"**Resolution:** {ticket['resolution']}")

    st.divider()
    st.subheader("🧠 Investigation Report")

    with st.spinner("🧠 Orchestrator generating full investigation report..."):
        report = orchestrator.investigate(incident)

    st.markdown(report)

    st.divider()
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="incident_investigation_report.md",
        mime="text/markdown"
    )

elif investigate_btn and not incident:
    st.warning("⚠️ Please enter an incident description first.")

st.divider()
st.markdown(
    "*Built with Azure OpenAI GPT-4o | ChromaDB | Multi-Agent Architecture | Microsoft Build AI Hackathon 2026*"
)
