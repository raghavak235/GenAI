 “Agentic Copilot” using the ChatGPT API (OpenAI’s gpt-3.5-turbo or gpt-4 models)"

import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def basic_chat_loop():
    """
    A minimal ChatGPT-based loop that just sends user messages,
    receives responses, and prints them out.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("Welcome to Agentic Copilot! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Append user message
        messages.append({"role": "user", "content": user_input})

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )

        # Extract assistant message
        assistant_reply = response["choices"][0]["message"]["content"]
        print(f"Agentic Copilot: {assistant_reply}\n")

        # Append assistant message to conversation
        messages.append({"role": "assistant", "content": assistant_reply})

Adding “Agentic” Capabilities
  Parse the user query.
  Decide if it needs to call an external tool (API, function, calculator, web search).
  Use the tool results to form a final answer

`  def weather_tool(location: str) -> str:
    """Fetch weather data for a location (dummy example or real API call)."""
    # For a real call, you'd do something like:
    # response = requests.get(f"http://api.weatherapi.com/v1/current.json?key=...&q={location}")
    # data = response.json()
    # return f"The weather in {location} is {data['current']['condition']['text']}, {data['current']['temp_c']} °C"
    return f"Tool says: It's always sunny in {location} (dummy response)."

A Prompting Strategy for Tool Usage
  We give the model a system message describing the available tools and how to use them.
  We read the assistant’s messages to see if it wants to call a tool.
  For instance, we look for a special format like {"tool": "calculator", "input": "2+2"}.
  If we detect such a message, we call that tool function on the back end.
  We inject the tool response back into the conversation for the model to use, and continue.
    
import json

system_message = """You are an agent with access to the following tools:
1) Calculator: to evaluate math expressions.
2) Weather: to provide weather info.

When you want to use a tool, return a JSON with:
{"tool": "<tool_name>", "input": "..."}
Otherwise, if you have a final answer for the user, return:
{"answer": "Your answer here"}

Use the tools step by step to arrive at your final answer if needed.
"""

def agentic_chat_loop():
    messages = [{"role": "system", "content": system_message}]
    print("Agentic Copilot with Tools! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user message
        messages.append({"role": "user", "content": user_input})

        # Call ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )

        assistant_reply = response.choices[0].message["content"].strip()

        # Try to parse the assistant's reply as JSON
        try:
            parsed = json.loads(assistant_reply)
        except json.JSONDecodeError:
            # If it can't parse, just show the raw assistant reply
            print(f"Agentic Copilot: {assistant_reply}\n")
            messages.append({"role": "assistant", "content": assistant_reply})
            continue

        # Check if the model wants to use a tool or is giving a final answer
        if "tool" in parsed:
            tool_name = parsed["tool"]
            tool_input = parsed["input"]

            if tool_name.lower() == "weather":
                tool_result = weather_tool(tool_input)
            else:
                tool_result = f"Tool {tool_name} not recognized."

            # Provide the tool result back to the model for further reasoning
            tool_message = f"Tool [{tool_name}] returned: {tool_result}"
            print(f"[Tool usage] {tool_message}")

            # Now the assistant needs to incorporate this result.
            # We add a new system or assistant message with the tool output:
            messages.append({"role": "assistant", "content": tool_message})
        elif "answer" in parsed:
            final_answer = parsed["answer"]
            print(f"Agentic Copilot: {final_answer}\n")
            messages.append({"role": "assistant", "content": final_answer})
        else:
            # If it's a weird structure, just show it
            print(f"Agentic Copilot: {assistant_reply}\n")
            messages.append({"role": "assistant", "content": assistant_reply})


