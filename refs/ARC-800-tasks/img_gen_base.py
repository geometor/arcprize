import json
import os
import glob
from PIL import Image, ImageDraw
import base64
import io

# Color mapping (adjust as needed)
COLOR_MAP = {
    0: (255, 255, 255),  # White
    1: (0, 0, 255),      # Blue
    2: (0, 255, 0),      # Green
    3: (255, 0, 0),      # Red
    4: (255, 255, 0),    # Yellow
    5: (255, 0, 255),    # Magenta
    6: (0, 255, 255),    # Cyan
    7: (255, 128, 0),    # Orange
    8: (128, 0, 128),    # Purple
    9: (0, 128, 0)       # Dark Green
}

def create_grid_image(grid):
    cell_size = 8
    width = len(grid[0]) * cell_size
    height = len(grid) * cell_size
    
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)
    
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = COLOR_MAP.get(cell, (128, 128, 128))  # Default to gray if color not found
            draw.rectangle([x*cell_size+1, y*cell_size+1, (x+1)*cell_size-1, (y+1)*cell_size-1], fill=color)
    
    return image

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def process_puzzle(puzzle_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    base64_data = {}
    
    for i, example in enumerate(puzzle_data['train']):
        input_image = create_grid_image(example['input'])
        output_image = create_grid_image(example['output'])
        
        input_image.save(os.path.join(output_dir, f'train_{i+1}_input.png'))
        output_image.save(os.path.join(output_dir, f'train_{i+1}_output.png'))
        
        base64_data[f'train_{i+1}_input'] = image_to_base64(input_image)
        base64_data[f'train_{i+1}_output'] = image_to_base64(output_image)
    
    for i, test in enumerate(puzzle_data['test']):
        input_image = create_grid_image(test['input'])
        input_image.save(os.path.join(output_dir, f'test_{i+1}_input.png'))
        base64_data[f'test_{i+1}_input'] = image_to_base64(input_image)
        
        if 'output' in test:
            output_image = create_grid_image(test['output'])
            output_image.save(os.path.join(output_dir, f'test_{i+1}_output.png'))
            base64_data[f'test_{i+1}_output'] = image_to_base64(output_image)
    
    # Save base64 data to a JSON file
    with open(os.path.join(output_dir, 'base64_images.json'), 'w') as f:
        json.dump(base64_data, f)

def process_all_puzzles(input_dir, output_base_dir):
    for json_file in glob.glob(os.path.join(input_dir, '*.json')):
        puzzle_name = os.path.splitext(os.path.basename(json_file))[0]
        output_dir = os.path.join(output_base_dir, puzzle_name)
        
        with open(json_file, 'r') as f:
            puzzle_data = json.load(f)
        
        process_puzzle(puzzle_data, output_dir)
        print(f"Processed puzzle: {puzzle_name}")

def main():
    input_dir = 'training'  # Directory containing JSON files
    output_base_dir = 'puzzle_images'  # Base directory for output images
    
    process_all_puzzles(input_dir, output_base_dir)
    print(f"All puzzles processed. Images and base64 data generated in {output_base_dir}")

if __name__ == "__main__":
    main()
