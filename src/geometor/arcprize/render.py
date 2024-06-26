import matplotlib.pyplot as plt
from typing import Optional, Tuple
from geometor.render import Plotter
from geometor.arcprize.model import Grid, ARCPuzzle
from geometor.arcprize.styles import ARC_STYLES

def setup_plotter(name: str, fig_size: Tuple[int, int] = (16, 9)) -> Plotter:
    plotter = Plotter(name, FIG_W=fig_size[0], FIG_H=fig_size[1])
    plotter.add_styles(ARC_STYLES)
    return plotter

def render_grid(plotter: Plotter, grid: Grid, title: Optional[str] = None):
    model = grid.to_geometor_model()
    plotter.plot_model(model)
    
    # Add grid lines
    for x in range(grid.width + 1):
        plt.axvline(x, color='gray', linewidth=0.5)
    for y in range(grid.height + 1):
        plt.axhline(y, color='gray', linewidth=0.5)
    
    plt.xlim(0, grid.width)
    plt.ylim(0, grid.height)
    plt.gca().invert_yaxis()  # Invert y-axis to match ARC grid orientation
    
    if title:
        plt.title(title)

def render_puzzle(puzzle: ARCPuzzle, output_path: Optional[str] = None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    plt.sca(ax1)
    input_plotter = setup_plotter("Input Grid")
    render_grid(input_plotter, puzzle.input, "Input")
    
    plt.sca(ax2)
    output_plotter = setup_plotter("Output Grid")
    render_grid(output_plotter, puzzle.output, "Output")
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
    else:
        plt.show()

def render_puzzle_sequence(puzzle: ARCPuzzle, output_path: Optional[str] = None):
    from geometor.render import Sequencer
    
    sequencer = Sequencer(f"ARC_Puzzle_Sequence")
    
    # Render input grid
    input_model = puzzle.input.to_geometor_model()
    sequencer.add_step(input_model, "Input Grid")
    
    # TODO: Add intermediate steps showing the transformation
    # This would require additional logic to determine the transformation steps
    
    # Render output grid
    output_model = puzzle.output.to_geometor_model()
    sequencer.add_step(output_model, "Output Grid")
    
    if output_path:
        sequencer.save(output_path)
    else:
        sequencer.show()

def render_analysis(puzzle: ARCPuzzle, analysis_result: dict, output_path: Optional[str] = None):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 20))
    
    # Render input grid
    plt.sca(ax1)
    input_plotter = setup_plotter("Input Grid")
    render_grid(input_plotter, puzzle.input, "Input")
    
    # Render output grid
    plt.sca(ax2)
    output_plotter = setup_plotter("Output Grid")
    render_grid(output_plotter, puzzle.output, "Output")
    
    # Render color analysis
    plt.sca(ax3)
    plt.title("Color Analysis")
    colors = analysis_result['colors']
    plt.bar(colors['input'].keys(), colors['input'].values(), alpha=0.5, label='Input')
    plt.bar(colors['output'].keys(), colors['output'].values(), alpha=0.5, label='Output')
    plt.legend()
    
    # Render other analysis results
    plt.sca(ax4)
    plt.title("Analysis Summary")
    plt.axis('off')
    summary = f"""
    Size:
      Input: {analysis_result['size']['input']}
      Output: {analysis_result['size']['output']}
      Difference: {analysis_result['size']['diff']}
    
    Symmetry:
      Input: {', '.join(analysis_result['input_symmetry'])}
      Output: {', '.join(analysis_result['output_symmetry'])}
    
    Patterns:
      Input: {len(analysis_result['input_patterns'])} patterns found
      Output: {len(analysis_result['output_patterns'])} patterns found
    """
    plt.text(0, 1, summary, verticalalignment='top')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
    else:
        plt.show()
