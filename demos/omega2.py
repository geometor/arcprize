import json
import os
import glob
from collections import Counter
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

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

def process_file(args):
    idx, file_path, output_dir = args
    data = load_data(file_path)
    base_name = os.path.basename(file_path).split(".")[0]
    base_name = f"{idx:03}-{base_name}"
    
    print(f"Processing {base_name}")
    generate_model(data, base_name, output_dir)
    
    return {
        "name": base_name,
    }

def main():
    input_dir = "../refs/ARC-800-tasks/training"
    output_dir = "./training"
    os.makedirs(output_dir, exist_ok=True)

    file_paths = glob.glob(os.path.join(input_dir, "*.json"))
    sorted_file_paths = sorted(file_paths, key=get_size_average)

    # Prepare arguments for multiprocessing
    args = [(idx, file_path, output_dir) for idx, file_path in enumerate(sorted_file_paths)]

    # Create a pool of workers
    num_workers = cpu_count()
    print(f"Using {num_workers} workers")

    with Pool(num_workers) as pool:
        results = pool.map(process_file, args)
    
    print(f"Processed {len(results)} files")

if __name__ == "__main__":
    main()
