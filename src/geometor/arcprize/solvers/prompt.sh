#!/usr/bin/env bash

function add_file() {
  printf "\n%s\n" "$1"
  printf "\`\`\`%s\n" "$2"
  cat "$1"
  printf "\`\`\`\n\n"
}

function main() {
  add_file ./gemini_solver.py python
  add_file ./gemini_logger.py python
  add_file ./gemini_client.py python
  echo
  cat prompt_instruction.md
}

main > prompt.txt
cat prompt.txt | xclip -selection clipboard
