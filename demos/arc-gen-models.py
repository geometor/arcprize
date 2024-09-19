"""
geometric modeler for the ARC challenge
processes for gathering information from input output matrices
each challenge has several training samples and one test
values in the matrix are integers from 0 to 9 - which we may refer to as colors
"""

import json
import os
import glob
from collections import Counter

from geometor.model import *
from geometor.model.helpers import *
from geometor.render import *

#  from geometor.divine import *


def generate_model(data, filename_prefix, output_dir):
    
    for idx, sample in enumerate(data["train"]):
        # input and out 
        for key, matrix in sample.items():

            model = Model(filename_prefix)
            for y, row in enumerate(matrix):
                for x, val in enumerate(row):

                    model.set_point(x, y, classes=[val], label=f"({x}-{y})")

            plotter = Plotter(model.name, FIG_W=9, FIG_H=9)
            plotter.plot_model(model)

            plt.show()



def plot_model(model):
    sequencer = Sequencer(model.name)
    #  sequencer.plot_sequence(model, extensions=['png'])
    sequencer.step_sequence(model)
    plt.show()


def analyze_model():

    #  print("\nfind golden sections in model: \n")
    #  sections, sections_by_line = find_golden_sections_in_model(model)
    #  print(f"sections: {len(sections)}")
    #  for section in sections:
        #  #  print(section.lengths)
        #  #  print(section.ratio)
        #  #  print(section.min_length)
        #  #  #  print(section.points)
        #  print(section.get_labels(model))

    #  chain_tree = find_chains_in_sections(sections)
    #  print(f"chains: {len(chain_tree)}")
    #  chains = unpack_chains(chain_tree)
    #  for chain in chains:
        #  labels = ["_".join(section.get_labels(model)) for section in chain.sections]
        #  print()
        #  print(labels)
        #  print(len(chain.sections))

        #  print("points: ", chain.points)
        #  print("lengths: ", chain.lengths)
        #  print("floats: ", chain.numerical_lengths)
        #  print("fibs: ", chain.fibonacci_labels)

    #  print('flow: ')
    #  for chain in chains:
        #  labels = ["_".join(section.get_labels(model)) for section in chain.sections]
        #  print(chain.count_symmetry_lines(), chain.flow)

    #  groups_by_size = group_sections_by_size(sections)
    #  print(groups_by_size)

    #  plotter = Plotter(model.name)
    #  plotter.plot_model(model)
    #  plot_sections(plotter, model, sections)
    
    #  plotter = Plotter(model.name)
    #  plotter.plot_model(model)
    #  plot_chains(plotter, model, chains)

    #  groups = group_sections_by_points(sections)
    #  plotter = Plotter(model.name)
    #  plotter.plot_model(model)
    #  title = "group sections by point"
    #  plot_groups(plotter, model, groups, title)

    #  plt.show()
    pass


def report_model(model):
    report_sequence(model)
    report_sequence_rst(model)



def report_sequence_rst(model, filename="model_report.rst"):
    """Generate a sequential RST report of the model."""
    with open(filename, 'w') as file:
        file.write(f"MODEL Report: {model.name}\n")
        file.write("=" * len(f"MODEL Report: {model.name}") + "\n\n")

        file.write(".. list-table:: Sequence\n")
        file.write("   :header-rows: 1\n\n")
        file.write("   * - Label\n     - <\n     - >\n     - Classes\n     - Parents\n     - Equation\n")

        for el, details in model.items():
            el_classes = ', '.join(details.classes.keys())
            el_parents = ', '.join(
                [f":math:`{model[parent].label}`" for parent in details.parents.keys()]
            )

            label = f":math:`{details.label}`"
            row = [
                label,
                "",
                "",
                el_classes,
                el_parents,
                "",
            ]
            if isinstance(el, spg.Point):
                row[1] = f":math:`{sp.latex(el.x)}`"
                row[2] = f":math:`{sp.latex(el.y)}`"

            elif isinstance(el, spg.Line):
                pt_1, pt_2 = el.points
                row[1] = f":math:`{model[pt_1].label or pt_1}`"
                row[2] = f":math:`{model[pt_2].label or pt_2}`"
                row[5] = f":math:`{sp.latex(el.equation())}`"

            elif isinstance(el, spg.Circle):
                pt_center = el.center
                pt_radius = details.pt_radius
                row[1] = f":math:`{model[pt_center].label or pt_center}`"
                row[2] = f":math:`{model[pt_radius].label or pt_radius}`"
                row[5] = f":math:`{sp.latex(el.equation())}`"

            elif isinstance(el, spg.Segment) or isinstance(el, spg.Polygon):
                vertices = ', '.join([f":math:`{model[pt].label or pt}`" for pt in el.vertices])
                row[1] = vertices

            file.write("   * - " + "\n     - ".join(row) + "\n")



"""
report engine for the ARC challenge
processes for gathering information from input output matrices
each challenge has several training samples and one test
values in the matrix are integers from 0 to 9 - which we may refer to as colors
"""

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


#  def generate_report(data, filename_prefix, output_dir):
    #  # FIM: add docstring
    #  report = []
    #  report.append(f"# {filename_prefix}")
    #  analyze_sizes(data, report)
    #  analyze_colors(data, report)

    #  report_content = "\n".join(report)
    #  filename = os.path.join(output_dir, f"{filename_prefix}.md")
    #  with open(filename, "w") as file:
        #  file.write(report_content)

def process_files(file_paths, output_dir):
    """
    Process multiple JSON files and generate a consolidated markdown report for each file.

    :param file_paths: List of paths to JSON files.
    :param output_dir: Directory where the markdown files will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sorted_file_paths = sorted(file_paths, key=get_size_average)

    for idx, file_path in enumerate(sorted_file_paths):
        data = load_data(file_path)
        base_name = os.path.basename(file_path).split(".")[0]
        generate_model(data, f"{idx:03}-{base_name}", output_dir)




if __name__ == "__main__":
    # Example usage
    file_paths = glob.glob("../refs/ARC-800-tasks/training/*.json")

    output_directory = "./training"
    process_files(file_paths, output_directory)
        

        
