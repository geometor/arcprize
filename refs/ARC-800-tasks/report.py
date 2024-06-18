import json
import os

def load_data(file_path):
    """
    Load JSON data from a file.

    :param file_path: Path to the JSON file.
    :return: Parsed JSON data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def analyze_sizes(data, report):
    """
    look for relations in input to output matrix sizes
    compare width, height, area 
    greater than, less than, equal
    """
    # TODO - return content for report - 

    report.append(f"## train sizes\n")
    for idx, (input_matrix, output_matrix) in enumerate([(sample["input"], sample["output"]) for sample in data["train"]]):

        report.append(f"|set|w|h|A|")
        report.append(f"|---|---|---|---|")

        input_width = len(input_matrix[0])
        input_height = len(input_matrix)
        input_area = input_width * input_height
        report.append(f"|input|{input_width}|{input_height}|{input_area}|")
        
        output_width = len(output_matrix[0])
        output_height = len(output_matrix)
        output_area = output_width * output_height
        report.append(f"|output|{output_width}|{output_height}|{output_area}|")
        report.append(f"|diff|{output_width - input_width}|{output_height - input_height}|{output_area - input_area}|")
        report.append("\n")


def generate_report(data, filename_prefix, output_dir):
    """
    Generate a consolidated report for all challenges in a file and save it to a markdown file.

    :param data: multiple train and one test data from the challenge
    :param filename_prefix: Prefix for the generated markdown file.
    :param output_dir: Directory where the markdown file will be saved.
    """
    report = []
    report.append(f"# {filename_prefix}")
    analyze_sizes(data, report)
    
    report_content = "\n".join(report)
    filename = os.path.join(output_dir, f"{filename_prefix}.md")
    with open(filename, 'w') as file:
        file.write(report_content)

def process_files(file_paths, output_dir):
    """
    Process multiple JSON files and generate a consolidated markdown report for each file.

    :param file_paths: List of paths to JSON files.
    :param output_dir: Directory where the markdown files will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_path in file_paths:
        data = load_data(file_path)
        #  train_challenges = data.get('train', [])
        #  test_challenges = data.get('test', [])
        
        base_name = os.path.basename(file_path).split('.')[0]
        
        # Generate a consolidated report for train and test challenges separately
        #  generate_report(train_challenges, f"{base_name}_train", output_dir)
        generate_report(data, f"{base_name}", output_dir)

# Example usage
file_paths = [
    './training/0a938d79.json',
    './training/0b148d64.json',
    './training/0ca9ddb6.json'
]

output_directory = './reports'
process_files(file_paths, output_directory)

