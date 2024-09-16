from vectordb import Memory
import json
import os
import pickle
def get_all_json_from_folder():
    folder = "/Users/joshs/Desktop/ai_stuff/geniza_stuff/data/book_1"
    
    # Create a Memory object
    memory = Memory(memory_file = '/Users/joshs/Desktop/ai_stuff/geniza_stuff/data/embeddings.pkl', chunking_strategy={'mode':'sliding_window', 'window_size': 126, 'overlap': 16})
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder, filename), 'r') as input_file:
                # Load the entire JSON file
                data = json.load(input_file)
                
                for page in data:
                    page_number = page["page_number"]
                    text = page["text"]
                    
                    # Save each page's text to the memory object
                    memory.save(text, metadata={"title": filename, "author": "S.D. Goitein", "page_number": page_number})
        else:
            continue
    return memory

# Call the function to execute it
memory = get_all_json_from_folder()
query = "Why is Cairo so important?"

results = memory.search(query, top_n=3)

print(results)