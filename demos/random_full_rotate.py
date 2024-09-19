from datetime import datetime
from rich import print

from geometor.arcprize.perception.experiment_runner import test_individual_puzzles
from geometor.arcprize.perception.data_export import export_to_csv
from geometor.arcprize.perception.puzzles.random_rotate import generate_puzzle_set


if __name__ == "__main__":
    model = "phi3:mini"
    #  model = "phi3:medium"
    #  model = "llama3.1"
    symbol_sets = ["digits", "letters", "symbols"]

    all_results = []

    for symbol_set in symbol_sets:
        puzzles = generate_puzzle_set(
            5,
            min_size=3,
            max_size=5,
            symbol_set_key=symbol_set,
            cell_delimiter="",
        )

        print(f"\nTesting with {symbol_set} symbol set:")

        results = test_individual_puzzles(puzzles, model)
        all_results.extend(results)

        correct_count = sum(1 for r in results if r["is_correct"])
        print(f"Individual testing: {correct_count} out of {len(puzzles)} correct")

        print("\nDetailed results:")
        for r in results:
            print(
                f"{r['index']}: Size: {r['size']}, Response: {r['model_response']}, Correct: {r['is_correct']}, Time: {r['processing_time']:.2f}s"
            )

    export_to_csv(
        all_results,
        f"rotation_puzzle_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    )

