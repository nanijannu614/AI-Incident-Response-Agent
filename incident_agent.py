from dotenv import load_dotenv
import os
import asyncio
from hindsight_client import Hindsight

load_dotenv()


def get_client():
    return Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=os.getenv("HINDSIGHT_API_KEY")
    )


async def analyze_incident_async(incident):

    client = get_client()

    query = f"""
You are an AI Incident Response Agent.

Current production incident:
{incident}

Use Hindsight's stored incident experiences, but follow these STRICT rules:

1. Only use a previous incident as evidence when BOTH are sufficiently similar:
   - The same service, dependency, or system component is involved.
   - The failure pattern or root cause is substantially similar.

2. Do NOT treat generic similarity such as "upstream service",
   "timeout", "503", or "overload" as enough evidence.

3. If the current incident involves a different service or dependency,
   explicitly say that no sufficiently similar previous incident was found.

4. Never copy a solution from an unrelated incident.

5. Provide:
   - Likely root cause
   - Recommended action
   - Why the action is relevant
   - Previous incident evidence, only when genuinely relevant

6. Clearly distinguish:
   - Relevant previous experience
   - Unrelated previous experience
   - New/unconfirmed diagnosis

Give a concise response suitable for a production engineer.
"""

    try:
        response = await client.areflect(
            bank_id="incident-response",
            query=query
        )

        return response.text

    finally:
        client.close()


def analyze_incident(incident):
    return asyncio.run(
        analyze_incident_async(incident)
    )


def close_client():
    pass