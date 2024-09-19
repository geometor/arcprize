import os
import matplotlib.pyplot as plt
from geometor.render import Plotter
from geometor.arcprize.styles import ARC_STYLES
from model import PuzzleSet, Puzzle, PuzzlePair, Grid
from multiprocessing import Pool, cpu_count

class ARCRenderer:
    def __init__(self, output_dir, fig_w=16, fig_h=9):
        self.output_dir = output_dir
        self.fig_w = fig_w
        self.fig_h = fig_h
        os.makedirs(output_dir, exist_ok=True)

    def render_grid(self, grid: Grid):
        plotter = Plotter(grid.name, FIG_W=self.fig_w, FIG_H=self.fig_h)
        plotter.add_styles(ARC_STYLES)
        plotter.plot_model(grid.model)
        output_path = os.path.join(self.output_dir, f"{grid.name}.png")
        plt.savefig(output_path)
        plt.close()

    def render_pair(self, pair: PuzzlePair):
        self.render_grid(pair.input)
        if pair.output:
            self.render_grid(pair.output)

    def render_puzzle(self, puzzle: Puzzle):
        for pair in puzzle.train:
            self.render_pair(pair)
        for pair in puzzle.test:
            self.render_pair(pair)

    def render_puzzle_set(self, puzzle_set: PuzzleSet):
        num_workers = cpu_count()
        print(f"Using {num_workers} workers")

        with Pool(num_workers) as pool:
            pool.map(self.render_puzzle, puzzle_set.puzzles)

def process_puzzle_set(args):
    input_dir, output_dir = args
    puzzle_set = PuzzleSet(input_dir)
    renderer = ARCRenderer(output_dir)
    renderer.render_puzzle_set(puzzle_set)
    return f"Processed {len(puzzle_set.puzzles)} puzzles"

def main():
    input_dir = "../refs/ARC-800-tasks/training"
    output_dir = "./rendered_puzzles"

    args = (input_dir, output_dir)
    result = process_puzzle_set(args)
    print(result)

if __name__ == "__main__":
    main()
