from mem0 import Memory
from openai import OpenAI
import json

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": "",
            "model": "text-embedding-004"
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": "",
            "model": "gemini-2.5-flash-lite"
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "C1SMwzwc0L-WGyvJCACkrTfORDs0Yq3IH4nxND6Y-Ns"
        }
    },
   "vector_store": {
    "provider": "qdrant",
    "config": {
        "host": "localhost",
        "port": 6333,
       
        "embedding_model_dims": 768
    }
}
}

mem_client = Memory.from_config(config)

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

USER_ID = "soham123"

while True:
    user_query = input("please enter something> ")

    search_memo = mem_client.search(
        query=user_query,
        user_id=USER_ID
    )

    results = search_memo.get("results", [])

    if results:
        print("🔍 Retrieving memories from vector DB...")
        for mem in results:
            print(f"- {mem.get('memory')}")
    else:
        print("ℹ️ No relevant memories found.")

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in results
    ]

    SYSTEM_PROMPT = f"Here is the context about the user: {json.dumps(memories)}"

    response = client.chat.completions.create(
        model="gemini-2.5-flash-lite",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},  
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content
    print("\n🤖 AI Response:")
    print(ai_response)

    mem_client.add(
    user_id=USER_ID,
    messages=[
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": ai_response}
    ]
)

    print("💾 Memory has been saved successfully.\n")
