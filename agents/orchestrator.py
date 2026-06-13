import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from agents.sop_agent import SOPAgent
from agents.ticket_agent import TicketAgent

load_dotenv()

class IncidentOrchestrator:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )
        self.sop_agent = SOPAgent()
        self.ticket_agent = TicketAgent()

    def investigate(self, incident_description):
        print("🔍 Step 1: Querying SOP Agent...")
        sop_context = "\n\n".join(self.sop_agent.retrieve(incident_description))

        print("🎫 Step 2: Querying Ticket Agent...")
        ticket_context = self.ticket_agent.get_resolutions(incident_description)

        print("🧠 Step 3: Generating Investigation Report...")
        prompt = f"""You are an expert AI Incident Investigation Copilot.

INCIDENT:
{incident_description}

RELEVANT SOPs:
{sop_context}

{ticket_context}

Generate a structured incident investigation report with exactly these sections:

## 1. INCIDENT CLASSIFICATION
(Type, Severity, Affected System)

## 2. PROBABLE ROOT CAUSES
(Top 3 ranked by likelihood. For each, include:
- Root cause description
- Confidence score as percentage (e.g. 85%)
- One line reasoning for the confidence level)

## 3. INVESTIGATION STEPS
(Step by step actions to diagnose)

## 4. RECOMMENDED ACTIONS
(Immediate remediation steps)

## 5. ESCALATION GUIDANCE
(Who to escalate to and when)

## 6. VERIFICATION CHECKLIST
(How to confirm the incident is resolved)

Be specific, actionable, and concise."""

        response = self.client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    orchestrator = IncidentOrchestrator()

    # Load data first
    print("📚 Loading SOPs and Tickets...")
    orchestrator.sop_agent.load_sops()
    orchestrator.ticket_agent.load_tickets()

    test_incident = "Users are unable to login. VPN authentication failures increasing. MFA prompts timing out."
    print("\n" + "="*60)
    print("INCIDENT:", test_incident)
    print("="*60 + "\n")

    report = orchestrator.investigate(test_incident)
    print(report)
