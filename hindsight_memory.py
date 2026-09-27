from dotenv import load_dotenv
import os
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)


def get_similar_incidents(incident):
    results = client.recall(
        bank_id="incident-response",
        query=incident
    )

    memories = []

    for result in results.results:
        memories.append(result.text)

    return memories


def record_incident_outcome(incident, root_cause, solution, outcome):
    memory = f"""
Production incident:
{incident}

Root cause:
{root_cause}

Solution applied:
{solution}

Outcome:
{outcome}
"""

    client.retain(
        bank_id="incident-response",
        content=memory
    )

    print("\nIncident outcome stored in Hindsight.")


def close_client():
    client.close()