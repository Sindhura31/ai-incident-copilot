# 🚨 AI Incident Investigation Copilot

> Microsoft Build AI Hackathon 2026 | Theme 05 — Agent Swarms

An AI-powered multi-agent system that assists operations engineers during incident investigation by analyzing incident descriptions and generating structured investigation guidance using SOPs and historical ticket data.

---

## 🎯 Problem Statement

Enterprise operations teams spend significant time investigating incidents by manually correlating alarms, logs, tickets, and SOPs. This process is slow, inconsistent, and heavily dependent on individual experience — leading to increased MTTR and unnecessary escalations.

---

## 💡 Solution

A multi-agent AI copilot that takes an incident description as input and instantly generates:

1. Incident Classification
2. Probable Root Causes (ranked)
3. Investigation Steps
4. Recommended Actions
5. Escalation Guidance
6. Verification Checklist

---

## 🏗️ Architecture

Incident Description (Input)
         ↓
    ┌─────────────────────────────────┐
    │         CrewAI Agent Swarm      │
    │                                 │
    │  🤖 SOP Retrieval Agent         │
    │     (ChromaDB RAG on SOPs)      │
    │           ↓                     │
    │  🤖 Historical Ticket Agent     │
    │     (ChromaDB Similarity Search)│
    │           ↓                     │
    │  🤖 Root Cause Analyst Agent    │
    │     (Evidence Analysis)         │
    │           ↓                     │
    │  🤖 Investigation Validator     │
    │     (Report Generation)         │
    └─────────────────────────────────┘
         ↓
  Structured Report:
1. Incident Classification
2. Probable Root Causes (with confidence %)
3. Investigation Steps
4. Recommended Actions
5. Escalation Guidance
6. Verification Checklist

---

## 🤖 AI Tools Used

- **Azure OpenAI GPT-4o** — LLM powering all 4 CrewAI agents
- **ChromaDB** — Vector database for SOPs and historical tickets
- **CrewAI** — Multi-agent orchestration framework (4-agent sequential swarm)
- **Streamlit** — UI framework
---
### 🤖 Agent Swarm Details
| Agent | Role |
|---|---|
| SOP Retrieval Specialist | Retrieves and analyzes relevant Standard Operating Procedures |
| Historical Ticket Analyst | Finds similar past incidents and resolution patterns |
| Root Cause Analyst | Ranks probable root causes with confidence levels |
| Investigation Validator | Generates final validated structured report |
## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- Azure OpenAI account with GPT-4o deployed

### Installation

```bash
git clone https://github.com/Sindhura31/ai-incident-copilot.git
cd ai-incident-copilot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI credentials:
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01

### Run

```bash
streamlit run app.py
```

---

## 👥 Team

| Name | Role |
|---|---|
| Sindhura | AI Engineer & Full Stack Developer |
| Anay | AI Engineer & Full Stack Developer  |
| Sonali | AI Engineer & Full Stack Developer  |

---

## 🗺️ Enterprise Roadmap

- Similar incident retrieval with confidence scoring
- ServiceNow and Jira integration
- Audit trail and governance controls
- Multi-tenant enterprise deployment
- Human approval checkpoints