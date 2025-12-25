# Chain Of Thought AI Agent

from openai import OpenAI
import requests
from pydantic import BaseModel, Field
from typing import Optional
import json
import os

client = OpenAI(
    api_key="your api key",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


def run_command(cmd: str):   
    import subprocess
    return subprocess.getoutput(cmd)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

def write_file(raw_input: str):
    """Creates a file. First line = file path, rest = content"""
    lines = raw_input.split("\n", 1)
    file_path = lines[0].strip()
    content = lines[1] if len(lines) > 1 else ""

    
    if (content.startswith('"') and content.endswith('"')) or (content.startswith("'") and content.endswith("'")):
        content = content[1:-1]

    
    content = content.encode('utf-8').decode('unicode_escape')

    
    if ";" in content or "{" in content or "}" in content:
        content = content.replace("{", "{\n").replace("}", "\n}").replace(";", ";\n")
        content = "\n".join(line.strip() for line in content.splitlines() if line.strip())

   
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

   
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"File '{file_path}' created successfully."


available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
    "write_file": write_file
}


SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN, TOOL, OBSERVE, and OUTPUT steps.
Strictly follow the JSON format for outputs.
Available tools:
- get_weather(city: str)
- run_command(cmd: str)
- write_file(file_path + content)
"""


class MyOutputFormat(BaseModel):
    step: str = Field(..., description="Step: START, PLAN, TOOL, OBSERVE, OUTPUT")
    content: Optional[str] = Field(None, description="Optional content for the step")
    tool: Optional[str] = Field(None, description="Tool to call")
    input: Optional[str] = Field(None, description="Input for the tool")


message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("\n--- AI Agent Ready ---\n")

while True:
    user_query = input("👉🏻 ")
    message_history.append({"role": "user", "content": user_query})

    while True:
      
        response = client.chat.completions.parse(
            model="gemini-2.5-flash",
            response_format=MyOutputFormat,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})

     
        try:
            parsed_result = response.choices[0].message.parsed
        except Exception as e:
            print("❌ Failed to parse AI output:", e)
            break

        
        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        
        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue


        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool.strip()  
            tool_input = parsed_result.input
            print(f"🛠️: {tool_to_call} ({tool_input})")

            if tool_to_call in available_tools:
                tool_response = available_tools[tool_to_call](tool_input)
                print(f"🛠️ Output: {tool_response}")

               
                message_history.append({
                    "role": "assistant",
                    "content": json.dumps({
                        "step": "OBSERVE",
                        "tool": tool_to_call,
                        "input": tool_input,
                        "output": tool_response
                    })
                })
            else:
                print(f"❌ Tool '{tool_to_call}' not found!")
            continue

    
        if parsed_result.step == "OUTPUT":
            print("🤖", parsed_result.content)
            message_history.append({"role": "assistant", "content": raw_result})
            break
