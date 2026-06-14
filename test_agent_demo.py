from dotenv import load_dotenv
load_dotenv()  # This cleanly handles loading all your API keys behind the scenes

from app.agent import ProductionAgent
# ... leave everything else exactly the same


from app.agent import ProductionAgent

# Instantiate your compiled LangGraph workflow agent
agent = ProductionAgent()

queries = [
    "What is LangGraph in one sentence?",
    "What is 2 + 2?",
    "Explain the difference between RAG and fine-tuning in 2 sentences.",
]

print("=== STARTING AGENT WORKFLOW TEST ===")
print()

for query in queries:
    print(f"Question: {query}")
    result = agent.invoke(query)
    
    print(f"Response: {result['response'][:150]}...")
    print(f"Model used: {result['model_used']}")
    # This will print the error that forced it to transition to fallback!
    print(f"Captured Error: {result['error']}") 
    print()