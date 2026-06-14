import os
from openai import AzureOpenAI
from dotenv import load_dotenv
os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
os.environ["AZURE_API_BASE"] = "https://sindu-mqcee492-eastus2.cognitiveservices.azure.com"
os.environ["AZURE_API_VERSION"] = "2025-01-01-preview"
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# ── Azure LLM for CrewAI via litellm ──────────────────────
os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")
os.environ["AZURE_API_BASE"] = "https://sindu-mqcee492-eastus2.cognitiveservices.azure.com"
os.environ["AZURE_API_VERSION"] = "2025-01-01-preview"

azure_llm = LLM(
    model="azure/gpt-4o",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_base="https://sindu-mqcee492-eastus2.cognitiveservices.azure.com",
    api_version="2025-01-01-preview"
)

# ── CrewAI Agents ──────────────────────────────────────────
from agents.sop_agent import SOPAgent
from agents.ticket_agent import TicketAgent

sop_retriever = Agent(
    role="SOP Retrieval Specialist",
    goal="Retrieve and analyze the most relevant Standard Operating Procedures for the given incident",
    backstory="You are an expert in IT operations and standard procedures.",
    verbose=True,
    allow_delegation=False,
    llm=azure_llm
)

ticket_retriever = Agent(
    role="Historical Ticket Analyst",
    goal="Find similar past incidents and their resolutions from historical ticket database",
    backstory="You are an expert in analyzing historical incident patterns.",
    verbose=True,
    allow_delegation=False,
    llm=azure_llm
)

root_cause_analyst = Agent(
    role="Root Cause Analyst",
    goal="Analyze incident evidence and identify probable root causes",
    backstory="You are a senior incident investigator with deep expertise in IT systems.",
    verbose=True,
    allow_delegation=False,
    llm=azure_llm
)

validation_agent = Agent(
    role="Investigation Validator",
    goal="Validate findings and generate the final complete investigation report",
    backstory="You are a quality assurance expert who reviews incident investigation reports.",
    verbose=True,
    allow_delegation=False,
    llm=azure_llm
)

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

        task_sop = Task(
            description=f"""Analyze the following SOPs for this incident:
INCIDENT: {incident_description}
RETRIEVED SOPs: {sop_context}
Summarize the key SOP guidelines relevant to this incident.""",
            agent=sop_retriever,
            expected_output="A structured summary of relevant SOP guidelines."
        )

        task_ticket = Task(
            description=f"""Analyze historical tickets for this incident:
INCIDENT: {incident_description}
HISTORICAL TICKETS: {ticket_context}
Identify patterns and resolution strategies from past similar incidents.""",
            agent=ticket_retriever,
            expected_output="A structured summary of patterns and resolutions from historical tickets."
        )

        task_root_cause = Task(
            description=f"""Based on SOP analysis and historical ticket patterns,
identify probable root causes for this incident:
INCIDENT: {incident_description}
Provide top 3 ranked root causes with confidence levels and evidence.""",
            agent=root_cause_analyst,
            expected_output="Top 3 ranked root causes with confidence levels and evidence."
        )

        task_validate = Task(
            description=f"""Review all findings and generate the final validated 
investigation report for this incident:
INCIDENT: {incident_description}
Generate a complete structured report with:
## 1. INCIDENT CLASSIFICATION
## 2. PROBABLE ROOT CAUSES
## 3. INVESTIGATION STEPS
## 4. RECOMMENDED ACTIONS
## 5. ESCALATION GUIDANCE
## 6. VERIFICATION CHECKLIST""",
            agent=validation_agent,
            expected_output="A complete structured incident investigation report."
        )

        print("🤖 Running Agent Swarm via CrewAI...")
        crew = Crew(
            agents=[sop_retriever, ticket_retriever, root_cause_analyst, validation_agent],
            tasks=[task_sop, task_ticket, task_root_cause, task_validate],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)


if __name__ == "__main__":
    orchestrator = IncidentOrchestrator()
    print("📚 Loading SOPs and Tickets...")
    orchestrator.sop_agent.load_sops()
    orchestrator.ticket_agent.load_tickets()

    test_incident = "Users are unable to login. VPN authentication failures increasing. MFA prompts timing out."
    print("\n" + "="*60)
    print("INCIDENT:", test_incident)
    print("="*60 + "\n")

    report = orchestrator.investigate(test_incident)
    print(report)