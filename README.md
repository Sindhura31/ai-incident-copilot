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
Incident Input
↓
SOP Agent (RAG on procedure documents)
+
Ticket Agent (similarity search on past incidents)
↓
Orchestrator (combines both → GPT-4o)
↓
Structured Investigation Report

---

## 🤖 AI Tools Used

- **Azure OpenAI GPT-4o** — Report generation and reasoning
- **ChromaDB** — Vector database for SOPs and tickets
- **LangChain** — Embedding pipeline
- **CrewAI** — Agent orchestration framework
- **Streamlit** — UI framework

---

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

---

## 🗺️ Enterprise Roadmap

- Similar incident retrieval with confidence scoring
- ServiceNow and Jira integration
- Audit trail and governance controls
- Multi-tenant enterprise deployment
- Human approval checkpoints