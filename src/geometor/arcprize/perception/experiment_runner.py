from rich import print
from datetime import datetime

from puzzles.random_rotate import generate_puzzle_set
from models.ollama import generate_response


def test_individual_puzzles(puzzles, model):
    results = []
    for i, prompt, correct_answer, size, symbol_set, input_grid, output_grid in puzzles:
        print("\n#####################################")
        print(prompt)
        result, processing_time = generate_response(prompt, model)
        response = result["response"].strip().lower()
        print(response)

        is_correct = response == correct_answer.lower()
        print(is_correct, correct_answer)

        test_result = {
            "index": i,
            "size": size,
            "model_response": response,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "processing_time": processing_time,
            "model": model,
            "symbol_set": symbol_set,
        }
        results.append(test_result)

    return results


def run_experiments(symbol_sets, puzzles_per_set, min_size, max_size, model):
    all_results = []

    for symbol_set in symbol_sets:
        puzzles = generate_puzzle_set(
            puzzles_per_set,
            min_size=min_size,
            max_size=max_size,
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

    return all_results
