from datetime import datetime

from experiment_runner import run_experiments
from data_export import export_to_csv

if __name__ == "__main__":
    model = "phi3:mini"
    symbol_sets_to_test = ["digits", "letters", "symbols"]
    results = run_experiments(
        symbol_sets_to_test, puzzles_per_set=3, min_size=3, max_size=5, model=model
    )

    export_to_csv(
        results,
        f"rotation_puzzle_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    )
