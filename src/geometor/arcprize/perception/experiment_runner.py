from rich import print
from datetime import datetime

from .puzzles.random_rotate import generate_puzzle_set
from .models.ollama import generate_response


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


