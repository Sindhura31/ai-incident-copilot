import os
import chromadb
from chromadb.utils import embedding_functions
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

class SOPAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )
        self.chroma_client = chromadb.PersistentClient(path="/tmp/chroma_db")
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.chroma_client.get_or_create_collection(
            name="sop_documents",
            embedding_function=self.embedding_fn
        )

    def load_sops(self, sop_folder="./data/sops"):
        documents = []
        ids = []
        for i, filename in enumerate(os.listdir(sop_folder)):
            if filename.endswith(".txt"):
                filepath = os.path.join(sop_folder, filename)
                with open(filepath, "r") as f:
                    content = f.read()
                documents.append(content)
                ids.append(f"sop_{i}")
                print(f"Loaded: {filename}")
        if documents:
            self.collection.upsert(documents=documents, ids=ids)
            print(f"\n✅ {len(documents)} SOPs loaded into ChromaDB")

    def retrieve(self, incident_description, n_results=2):
        results = self.collection.query(
            query_texts=[incident_description],
            n_results=n_results
        )
        return results["documents"][0]

    def analyze(self, incident_description):
        relevant_sops = self.retrieve(incident_description)
        sop_context = "\n\n---\n\n".join(relevant_sops)
        prompt = f"""You are an expert incident response assistant.

Incident Description:
{incident_description}

Relevant SOPs:
{sop_context}

Based on the SOPs above, provide:
1. Incident Classification
2. Probable Root Causes (top 3, ranked)
3. Investigation Steps (from SOP)
4. Recommended Actions
5. Escalation Guidance
6. Verification Checklist

Be specific and actionable."""
        response = self.client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    agent = SOPAgent()
    agent.load_sops()
    test_incident = "Users are unable to login. VPN authentication failures increasing. MFA prompts timing out."
    print("\n" + "="*50)
    print("INCIDENT:", test_incident)
    print("="*50)
    result = agent.analyze(test_incident)
    print(result)
