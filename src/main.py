import asyncio
from src.llm.base import GeminiService


async def main():
    print("Welcome to Viazuri Travel Concierge!\n")
    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        response, history = await GeminiService.get_response(user_input, history)
        print("\nViazuri:", response or "No response\n")


def dev():
    asyncio.run(main())

