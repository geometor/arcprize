import json
import os
import glob
from collections import Counter
import matplotlib.pyplot as plt


from geometor.model import Model
from geometor.model.helpers import *
from geometor.render import Plotter, Sequencer


def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def generate_model(data, filename_prefix, output_dir):
    for idx, sample in enumerate(data["train"]):
        for key, matrix in sample.items():
            model = Model(f"{filename_prefix}_{idx}_{key}")
            print(model.name)
            for y, row in enumerate(matrix):
                for x, val in enumerate(row):
                    model.set_point(x, y, classes=[str(val)], label=f"({x},{y})")
            
            x = x if x > 1 else 2
            y = y if y > 1 else 2
            plotter = Plotter(model.name, FIG_W=16, FIG_H=9)
            plotter.plot_model(model)
            plt.savefig(os.path.join(output_dir, f"{model.name}.png"))
            plt.close()

def analyze_colors(data):
    color_analysis = []
    for idx, sample in enumerate(data["train"]):
        input_colors = Counter([val for row in sample["input"] for val in row])
        output_colors = Counter([val for row in sample["output"] for val in row])
        
        color_diff = {color: output_colors[color] - input_colors[color] 
                      for color in set(input_colors) | set(output_colors)}
        
        color_analysis.append({
            "sample": idx,
            "input_colors": dict(input_colors),
            "output_colors": dict(output_colors),
            "color_diff": color_diff
        })
    
    return color_analysis

def analyze_sizes(data):
    size_analysis = []
    for idx, sample in enumerate(data["train"]):
        input_size = (len(sample["input"][0]), len(sample["input"]))
        output_size = (len(sample["output"][0]), len(sample["output"]))
        
        size_analysis.append({
            "sample": idx,
            "input_size": input_size,
            "output_size": output_size,
            "size_diff": (output_size[0] - input_size[0], output_size[1] - input_size[1])
        })
    
    return size_analysis

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

def process_file(idx, file_path, output_dir):
    data = load_data(file_path)
    base_name = os.path.basename(file_path).split(".")[0]
    base_name = f"{idx:03}-{base_name}"
    
    print(base_name)
    generate_model(data, base_name, output_dir)
    #  color_analysis = analyze_colors(data)
    #  size_analysis = analyze_sizes(data)
    
    # TODO: Implement functions to analyze geometric patterns
    # geometric_analysis = analyze_geometric_patterns(data)
    
    return {
        "name": base_name,
        #  "color_analysis": color_analysis,
        #  "size_analysis": size_analysis,
        # "geometric_analysis": geometric_analysis
    }

def main():
    input_dir = "../refs/ARC-800-tasks/training"
    output_dir = "./training"
    os.makedirs(output_dir, exist_ok=True)

    file_paths = glob.glob(os.path.join(input_dir, "*.json"))
    sorted_file_paths = sorted(file_paths, key=get_size_average)

    results = []

    for idx, file_path in enumerate(sorted_file_paths):
        result = process_file(idx, file_path, output_dir)
        results.append(result)
    
    # TODO: Implement function to generate a comprehensive report
    # generate_report(results, output_dir)

if __name__ == "__main__":
    main()
