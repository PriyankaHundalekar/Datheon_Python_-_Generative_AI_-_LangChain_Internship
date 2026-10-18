import os
import json
from pathlib import Path
from dotenv import load_dotenv

from google import genai
from google.genai import types
from ddgs import DDGS  # Using direct 'ddgs' package

# 1. Environment Setup
env_path = Path(__file__).resolve().parent.parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path, override=True)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY could not be loaded!")

client = genai.Client(api_key=api_key)


# 2. Tool Functions
def web_search(query: str) -> str:
    """Search real-time facts and news on the internet using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            if not results:
                return "No search results found. Proceed with general knowledge."
            return "\n".join([f"- {r.get('title')}: {r.get('body')} ({r.get('href')})" for r in results])
    except Exception as e:
        return f"Search error: {str(e)}"


def python_calculator(expression: str) -> str:
    """Evaluate mathematical expressions or numerical calculations."""
    try:
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max, "pow": pow}
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


def local_file_reader(file_path: str) -> str:
    """Read raw text contents of a local file."""
    try:
        path = Path(file_path.strip("'\""))
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            return content if content else "File is empty."
    except Exception as e:
        return f"Error reading file: {str(e)}"


tool_map = {
    "web_search": web_search,
    "python_calculator": python_calculator,
    "local_file_reader": local_file_reader,
}

available_tools = [web_search, python_calculator, local_file_reader]


# 3. Execution Loop with Strict Step Controls
def run_autonomous_agent(user_query: str):
    print(f"\n🤖 Agent thinking about query: '{user_query}'...")

    chat = client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            temperature=0.0,
            tools=available_tools,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
            system_instruction=(
                "You are an efficient autonomous AI agent. "
                "CRITICAL INSTRUCTION: Use tools at most ONCE or TWICE to gather data. "
                "Synthesize your final answer immediately after observing tool outputs. "
                "Do NOT perform repetitive or looped tool calls."
            )
        )
    )

    response = chat.send_message(user_query)
    tool_call_count = 0

    # Max 3 iteration turns before forcing an answer
    for step in range(1, 4):
        if response.function_calls:
            for function_call in response.function_calls:
                tool_name = function_call.name
                tool_args = function_call.args
                tool_call_count += 1

                print(f"\n⚙️  [Tool Call] Invoking '{tool_name}' with arguments:")
                print(f"    {json.dumps(tool_args)}")

                # Run Tool
                if tool_name in tool_map:
                    tool_result = tool_map[tool_name](**tool_args)
                else:
                    tool_result = f"Error: Tool {tool_name} not found."

                print(f"📥 [Observation] Result received ({len(str(tool_result))} characters)")

                # If limit reached, tell agent to finalize answer immediately
                if tool_call_count >= 2:
                    tool_result += "\n\n[SYSTEM: Maximum tool call limit reached. Please provide your final answer now.]"

                # Send observation back to agent
                response = chat.send_message(
                    types.Part.from_function_response(
                        name=tool_name,
                        response={"result": tool_result}
                    )
                )

                # Break out if we reached our cap
                if tool_call_count >= 2:
                    return response.text
        else:
            # Final text response from agent
            return response.text

    return response.text


# 4. Interactive Command Line Interface
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Multi-Tool Autonomous AI Agent Ready!")
    print(f"Available Tools: {list(tool_map.keys())}")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 60 + "\n")

    while True:
        user_input = input("Enter multi-step research query: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if not user_input:
            continue

        print("-" * 60)
        try:
            final_answer = run_autonomous_agent(user_input)
            print("\n📌 Final Answer:")
            print(final_answer)
        except Exception as e:
            print(f"\n❌ Error executing agent: {e}")
        print("-" * 60 + "\n")