"""
report engine for the ARC challenge
processes for gathering information from input output matrices
each challenge has several training samples and one test
values in the matrix are integers from 0 to 9 - which we may refer to as colors
"""

import json
import os
import glob
from collections import Counter

def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def analyze_colors(data, report):
    report.append(f"## Color Analysis\n")
    for idx, (input_matrix, output_matrix) in enumerate(
        [(sample["input"], sample["output"]) for sample in data["train"]]
    ):
        input_colors = Counter([val for row in input_matrix for val in row])
        output_colors = Counter([val for row in output_matrix for val in row])
        
        # Creating a markdown table for color counts
        report.append(f"|c|i|o|diff|")
        report.append(f"|---|---|---|---|")
        all_colors = set(input_colors.keys()).union(set(output_colors.keys()))
        for color in sorted(all_colors):
            diff = output_colors[color] - input_colors[color]
            report.append(f"|{color}|{input_colors[color]}|{output_colors[color]}|{diff}|")
        report.append("\n")

def analyze_sizes(data, report):
    report.append(f"## Train Sizes\n")
    for idx, (input_matrix, output_matrix) in enumerate(
        [(sample["input"], sample["output"]) for sample in data["train"]]
    ):
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
        report.append(
            f"|diff|{output_width - input_width}|{output_height - input_height}|{output_area - input_area}|"
        )
        report.append("\n")

def get_size_average(file_path):
    data = load_data(file_path)
    total_area = 0
    num_samples = len(data["train"])

    for sample in data["train"]:
        input_matrix = sample["input"]
        output_matrix = sample["output"]
        input_area = len(input_matrix) * len(input_matrix[0])
        output_area = len(output_matrix) * len(output_matrix[0])
        total_area += input_area + output_area

    return total_area / num_samples if num_samples > 0 else 0

def sort_filepaths(file_paths):
    return sorted(file_paths, key=get_size_average)

def generate_report(data, filename_prefix, output_dir):
    # FIM: add docstring
    report = []
    report.append(f"# {filename_prefix}")
    analyze_sizes(data, report)
    analyze_colors(data, report)

    report_content = "\n".join(report)
    filename = os.path.join(output_dir, f"{filename_prefix}.md")
    with open(filename, "w") as file:
        file.write(report_content)

def process_files(file_paths, output_dir):
    """
    Process multiple JSON files and generate a consolidated markdown report for each file.

    :param file_paths: List of paths to JSON files.
    :param output_dir: Directory where the markdown files will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sorted_file_paths = sort_filepaths(file_paths)

    for idx, file_path in enumerate(sorted_file_paths):
        data = load_data(file_path)
        base_name = os.path.basename(file_path).split(".")[0]
        generate_report(data, f"{idx:03}-{base_name}", output_dir)

# Example usage
file_paths = glob.glob("./training/*.json")

output_directory = "./reports"
process_files(file_paths, output_directory)

