from agent.agent_core import MultiMemoryAgent

def main():
    agent = MultiMemoryAgent()
    print("Welcome to Multi-Memory Agent Demo!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        response = agent.run(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()
