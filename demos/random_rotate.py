import json
from datetime import datetime
from rich import print
from rich.console import Console
from rich.table import Table

from geometor.arcprize.perception.experiment_runner import test_individual_puzzles
from geometor.arcprize.perception.data_export import export_to_csv
from geometor.arcprize.perception.puzzles.random_rotate import generate_puzzle_set
from geometor.arcprize.perception.render.svg import visualize_puzzles

def create_results_table(results, symbol_set):
    table = Table(title=f"Results for {symbol_set}")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Size", style="magenta")
    table.add_column("Response", style="green")
    table.add_column("Correct", style="yellow")
    table.add_column("Time (s)", style="blue")

    for r in results:
        table.add_row(
            str(r['index']),
            str(r['size']),
            r['model_response'],
            "✓" if r['is_correct'] else "✗",
            f"{r['processing_time']:.2f}"
        )

    return table

def export_to_json(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results exported to {filename}")

if __name__ == "__main__":
    console = Console()

    model = "phi3:mini"
    symbol_sets = ["digits", "letters", "symbols"]

    all_results = []
    run_metadata = {
        "model": model,
        "symbol_sets": symbol_sets,
        "timestamp": datetime.now().isoformat(),
        "results": []
    }

    for symbol_set in symbol_sets:
        puzzles = generate_puzzle_set(
            10,
            min_size=3,
            max_size=9,
            symbol_set_key=symbol_set,
            cell_delimiter="",
        )

        console.print(f"\n[bold]Testing with {symbol_set} symbol set:[/bold]")

        results = test_individual_puzzles(puzzles, model)
        all_results.extend(results)

        correct_count = sum(1 for r in results if r["is_correct"])
        console.print(f"Individual testing: {correct_count} out of {len(puzzles)} correct")

        table = create_results_table(results, symbol_set)
        console.print(table)

        # Add results to run metadata
        run_metadata["results"].extend(results)

    # Export to CSV
    csv_filename = f"rotation_puzzle_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    export_to_csv(all_results, csv_filename)

    # Export to JSON
    json_filename = f"rotation_puzzle_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    export_to_json(run_metadata, json_filename)

    # Print summary
    console.print("\n[bold]Summary:[/bold]")
    total_correct = sum(1 for r in all_results if r["is_correct"])
    total_puzzles = len(all_results)
    console.print(f"Total correct: {total_correct} out of {total_puzzles} ({total_correct/total_puzzles:.2%})")

    # Print average processing time
    avg_time = sum(r["processing_time"] for r in all_results) / len(all_results)
    console.print(f"Average processing time: {avg_time:.2f} seconds")

    visualize_puzzles(json_filename)
