from rich import print
from datetime import datetime

from .puzzles.random_rotate import generate_puzzle_set
from .models.ollama import generate_response
from .grids.tools import grid_to_string


def test_individual_puzzles(puzzles, model):
    results = []
    for i, prompt, correct_answer, size, symbol_set, input_grid, output_grid in puzzles:
        input_grid_str = grid_to_string(input_grid)
        output_grid_str = grid_to_string(output_grid)
        print(f"\n {i} of {len(puzzles)} #####################################")
        print()
        print(input_grid_str)
        print()
        print(output_grid_str)
        result, processing_time = generate_response(prompt, model)

        response = result["response"].strip().lower()
        print(f"response: {response}")

        is_correct = response == correct_answer.lower()
        print(f"  answer: {correct_answer}", is_correct)

        print(f"    time: {processing_time:.2f} s")

        test_result = {
            "index": i,
            "size": size,
            "model_response": response,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "processing_time": processing_time,
            "model": model,
            "symbol_set": symbol_set,
            "input_grid": grid_to_string(input_grid),
            "output_grid": grid_to_string(output_grid),
        }
        results.append(test_result)

    return results


