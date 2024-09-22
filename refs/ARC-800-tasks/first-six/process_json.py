import json
import os

def stack_grid(grid):
    return [' '.join(map(str, row)) for row in grid]

def process_arc_json(file_path):
    stem = os.path.splitext(os.path.basename(file_path))[0]
    os.makedirs(stem, exist_ok=True)
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    stacked_data = {key: [] for key in data}
    
    for set_name in ['test', 'train']:
        if set_name in data:
            for idx, example in enumerate(data[set_name]):
                process_example(stem, set_name, idx, example)
                stacked_example = {
                    "input": stack_grid(example['input']),
                    "output": stack_grid(example['output']) if 'output' in example else []
                }
                stacked_data[set_name].append(stacked_example)
    
    # Write the full stacked JSON
    with open(f"{stem}_stacked.json", 'w') as f:
        json.dump(stacked_data, f, indent=2)

def process_example(stem, set_name, idx, example):
    output_file = f"{stem}/{set_name}_{idx}.json"
    
    stacked_example = {
        "input": stack_grid(example['input']),
        "output": stack_grid(example['output']) if 'output' in example else []
    }
    
    with open(output_file, 'w') as f:
        json.dump(stacked_example, f, indent=2)

if __name__ == "__main__":
    for file in os.listdir('.'):
        if file.endswith('.json'):
            print(f"Processing {file}...")
            process_arc_json(file)

print("Processing complete. Check the output folders and stacked JSONs.")
