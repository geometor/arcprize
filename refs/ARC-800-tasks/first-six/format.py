import json

def format_grid(grid):
    return '[\n' + ',\n'.join(['    [' + ', '.join(map(str, row)) + ']' for row in grid]) + '\n  ]'

def process_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    for set_type in ['train', 'test']:
        for example in data[set_type]:
            example['input'] = json.loads(format_grid(example['input']))
            example['output'] = json.loads(format_grid(example['output']))
    
    return json.dumps(data, indent=2)

def main():
    input_file = '3aa6fb7a.json'
    output_file = '3aa6fb7a_formatted.json'
    
    formatted_data = process_json(input_file)
    
    with open(output_file, 'w') as f:
        f.write(formatted_data)
    
    print(f"Formatted data written to {output_file}")

if __name__ == "__main__":
    main()
