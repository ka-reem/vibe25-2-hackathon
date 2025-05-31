#!/usr/bin/env python3
"""
Super simple chat interface for person_data.json
Just load the data and ask questions about it!
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Simple chat with person_data.json"""
    
    # Initialize the OpenAI client with Llama API
    client = OpenAI(
        api_key=os.environ.get("LLAMA_API_KEY"), 
        base_url="https://api.llama.com/compat/v1/"
    )
    
    # Load person data
    try:
        with open("person_data.json", 'r', encoding='utf-8') as f:
            person_data = json.load(f)
        print("✅ Loaded person_data.json successfully!")
    except FileNotFoundError:
        print("❌ person_data.json not found. Please run 'python crustdata.py' first.")
        return
    except json.JSONDecodeError:
        print("❌ Invalid JSON in person_data.json")
        return
    
    # Handle list format from CrustData API
    if isinstance(person_data, list) and len(person_data) > 0:
        person = person_data[0]  # Get the first person
    else:
        person = person_data
    
    print("\n🤖 Ask me anything about the person data!")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_question = input("You: ").strip()
        
        if user_question.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_question:
            continue
        
        # Create a simple prompt
        prompt = f"""
        Based on the following person data, please answer the user's question:

        Person Data:
        {json.dumps(person, indent=2)}

        User Question: {user_question}

        Please provide a helpful and accurate answer based on the data above.
        """
        
        try:
            completion = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            response = completion.choices[0].message.content
            print(f"\n🤖 Assistant: {response}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

if __name__ == "__main__":
    main()
