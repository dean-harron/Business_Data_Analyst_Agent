from agent.agent import run_agent

result = run_agent(
    "Analyze revenue and profits by region and tell me which region deserves attention.",
    "data/sample_business.csv",
)
print(result["messages"][-1])