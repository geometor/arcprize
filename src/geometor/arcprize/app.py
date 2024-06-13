"""
run the main app
"""
from .arcprize import Arcprize


def run() -> None:
    reply = Arcprize().run()
    print(reply)
