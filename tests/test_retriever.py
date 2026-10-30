from datetime import datetime, timezone
from aegis.knowledge.retriever import TemporalRetriever

print("--- RAG Test 1: Querying a Historical Dispute (March 12, 2024) ---")
# Customer disputes a fee from March 2024
historical_date = datetime(2024, 3, 12, tzinfo=timezone.utc)
historical_citations = TemporalRetriever.retrieve_policy("What is the mortgage late fee?", point_in_time=historical_date)

for citation in historical_citations:
    print(f"Title:   {citation.document_title}")
    print(f"Snippet: {citation.snippet}")


print("\n--- RAG Test 2: Querying Today's Active Policy ---")
# Customer asks about a fee today
current_citations = TemporalRetriever.retrieve_policy("What is the mortgage late fee?")

for citation in current_citations:
    print(f"Title:   {citation.document_title}")
    print(f"Snippet: {citation.snippet}")