from src.knowledge_bot import build_knowledge_agent

def main():
    agent = build_knowledge_agent()
    print("Conversational Knowledge Bot (type 'exit' to quit)\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        ans = agent.run(q)
        print(f"\nBot: {ans}\n")

if __name__ == "__main__":
    main()
