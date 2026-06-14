import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

class TicketAgent:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="/tmp/chroma_db")
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.chroma_client.get_or_create_collection(
            name="ticket_documents",
            embedding_function=self.embedding_fn
        )

    def load_tickets(self, ticket_file="./data/tickets.csv"):
        df = pd.read_csv(ticket_file)
        documents = []
        ids = []
        metadatas = []
        for _, row in df.iterrows():
            documents.append(row["description"])
            ids.append(f"ticket_{row['id']}")
            metadatas.append({
                "resolution": row["resolution"],
                "category": row["category"]
            })
            print(f"Loaded ticket {row['id']}: {row['description'][:50]}...")
        if documents:
            self.collection.upsert(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print(f"\n✅ {len(documents)} tickets loaded into ChromaDB")

    def find_similar(self, incident_description, n_results=3):
        results = self.collection.query(
            query_texts=[incident_description],
            n_results=n_results
        )
        similar_tickets = []
        for i in range(len(results["documents"][0])):
            similar_tickets.append({
                "description": results["documents"][0][i],
                "resolution": results["metadatas"][0][i]["resolution"],
                "category": results["metadatas"][0][i]["category"]
            })
        return similar_tickets

    def get_resolutions(self, incident_description):
        similar = self.find_similar(incident_description)
        output = "SIMILAR PAST INCIDENTS AND RESOLUTIONS:\n\n"
        for i, ticket in enumerate(similar, 1):
            output += f"Past Incident {i}:\n"
            output += f"  Description: {ticket['description']}\n"
            output += f"  Resolution: {ticket['resolution']}\n"
            output += f"  Category: {ticket['category']}\n\n"
        return output


if __name__ == "__main__":
    agent = TicketAgent()
    agent.load_tickets()
    test_incident = "Users are unable to login. VPN authentication failures increasing. MFA prompts timing out."
    print("\n" + "="*50)
    print("INCIDENT:", test_incident)
    print("="*50)
    result = agent.get_resolutions(test_incident)
    print(result)
