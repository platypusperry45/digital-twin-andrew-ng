#!/usr/bin/env python3
"""
Interactive Terminal Demo for Digital Twin of Andrew Ng.

Provides a multi-turn conversation loop with session memory,
RAG retrieval, and persona consistency.
"""

import sys
import uuid
from backend.core.container import container


def print_banner():
    print("=" * 65)
    print("      Digital Twin of Andrew Ng - Interactive Terminal Demo")
    print("=" * 65)
    print("Type 'exit' or 'quit' to end the session.")
    print("Type 'clear' to reset conversation memory.")
    print("=" * 65 + "\n")


def main():
    # Initialize dependency container
    print("[*] Initializing Digital Twin agent and dependencies...")
    try:
        container.initialize()
    except Exception as e:
        print(f"[!] Initialization failed: {e}")
        print("[!] Please ensure GEMINI_API_KEYS is configured in your .env file.")
        sys.exit(1)

    session_id = f"demo_session_{uuid.uuid4().hex[:8]}"
    print(f"[*] Session started: {session_id}\n")

    print_banner()

    conv_service = container.conversation_service

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("\nAndrew Ng Twin: Keep learning, and remember—AI is the new electricity! Goodbye.")
                break

            if user_input.lower() == "clear":
                container.sessions.clear()
                session_id = f"demo_session_{uuid.uuid4().hex[:8]}"
                print(f"[*] Memory cleared. New session started: {session_id}\n")
                continue

            print("\nAndrew Ng Twin thinking...", end="\r")

            response = conv_service.chat(
                session_id=session_id,
                message=user_input,
            )

            print(" " * 40, end="\r")  # Clear thinking line
            print(f"Andrew Ng Twin:\n{response.response_text}\n")
            
            if hasattr(response, "sources") and response.sources:
                print(f"   [Citations / Sources Retrieved: {len(response.sources)}]")
            print("-" * 65 + "\n")

        except KeyboardInterrupt:
            print("\nExiting session...")
            break
        except Exception as err:
            print(f"\n[!] Error during conversation turn: {err}\n")


if __name__ == "__main__":
    main()