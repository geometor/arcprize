from geometor.arcprize.puzzles import Puzzle, PuzzleSet, Grid
from rich import print
from pathlib import Path
import json
import numpy as np
import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def add(a: float, b: float):
    """returns a + b."""
    return a + b


def subtract(a: float, b: float):
    """returns a - b."""
    return a - b


def multiply(a: float, b: float):
    """returns a * b."""
    return a * b


def divide(a: float, b: float):
    """returns a / b."""
    return a / b


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", tools=[add, subtract, multiply, divide]
)

print(model)

chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message(
    "I have 57 cats, each owns 44 mittens, how many mittens is that in total?"
)
print(response.text)

print(chat.history)
