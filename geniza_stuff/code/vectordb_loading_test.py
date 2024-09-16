from vectordb import Memory
import json
import os
import openai  # Import the OpenAI library

# Initialize the Memory object with the specified memory file
memory_file_path = '/Users/joshs/Desktop/ai_stuff/geniza_stuff/data/embeddings.pkl'
memory = Memory(memory_file=memory_file_path, chunking_strategy={'mode': 'sliding_window', 'window_size': 126, 'overlap': 16})

# Function to generate a complete answer using OpenAI's GPT-3
def generate_answer(prompt):
    openai.api_key = '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'  # Replace with your OpenAI API key
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    
    return completion.choices[0].text

def get_and_generate_answer(query, top_n=3):
    # Perform a search in the memory
    results = memory.search(query, top_n=top_n)

    # Create a prompt for GPT-3 using the search results
    prompt = f"Answer the question '{query}' as an expert in the Cairo Geniza using the following information:\n"
    for i, result in enumerate(results):
        prompt += f"{i + 1}. {result['metadata']['title']} (Page {result['metadata']['page_number']}):\n"
        prompt += result['chunk'] + "\n"

    # Generate a complete answer using GPT-3
    answer = generate_answer(prompt)
    #answer = prompt
    return answer

# Query and generate an answer
query = "Why is Cairo so important?"
answer = get_and_generate_answer(query)
print("Generated Answer:")
print(answer)


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
       {"role": "user", "content": "Explain how to assemble a PC"}
    ],
    functions=[
        {
          "name": "get_answer_for_user_query",
          "description": "Get user answer in series of steps",
        }
    ],
    function_call={"name": "get_answer_for_user_query"}
)

# parse JSON output from AI model
output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])